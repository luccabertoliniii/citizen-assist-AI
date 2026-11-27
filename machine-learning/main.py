"""
Coloque este .py na mesma pasta do CSV original e execute no VS Code.
Resultados (gráficos, tabelas e texto) são salvos em ./resultados.
Os dados são observacionais: associações não demonstram causalidade.
"""
from pathlib import Path
import warnings

import matplotlib
matplotlib.use('Agg')  # Salva gráficos sem depender de janela gráfica
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

PASTA = Path(__file__).resolve().parent
ARQUIVO = PASTA / 'IPS Brasil 2026 - Tabela de Dados_Brasil.csv'
SAIDA = PASTA / 'resultados'
SAIDA.mkdir(exist_ok=True)
sns.set_theme(style='whitegrid')

IPS = 'Índice de Progresso Social'
ACESSO = 'Acesso à Informação e Comunicação'
COBERTURA = 'Cobertura de Internet Móvel (4G/5G)'
BANDA = 'Densidade de Internet Banda Larga Fixa'
QUALIDADE = 'Qualidade de Internet Móvel'
EDUCACAO = 'Acesso ao Conhecimento Básico'
VARIAVEIS = [IPS, ACESSO, COBERTURA, BANDA, QUALIDADE, EDUCACAO]
relatorio = []

def registrar(texto=''):
    texto = str(texto)
    print(texto)
    relatorio.append(texto)

def figura(nome):
    plt.tight_layout()
    plt.savefig(SAIDA / nome, dpi=180, bbox_inches='tight')
    plt.close()

def resumo_modelo(modelo, nome):
    registrar(f'\n{nome}')
    registrar(f'Equação: {modelo.model.endog_names} = ' + ' + '.join(
        f'({coef:.5f}) × {variavel}' if variavel != 'const' else f'{coef:.5f}'
        for variavel, coef in modelo.params.items()))
    registrar(f'R² = {modelo.rsquared:.5f}; R² ajustado = {modelo.rsquared_adj:.5f}')
    registrar(f'Teste F = {modelo.fvalue:.5f}; p-valor = {modelo.f_pvalue:.8g}')
    registrar('Adequação global a 5%: ' + ('significativa' if modelo.f_pvalue < .05 else 'não significativa'))
    (SAIDA / f'{nome.replace(" ", "_").lower()}_resumo.txt').write_text(str(modelo.summary()), encoding='utf-8')

if not ARQUIVO.exists():
    raise FileNotFoundError(f'CSV não encontrado: {ARQUIVO}\nColoque-o na mesma pasta do script.')

df = pd.read_csv(ARQUIVO, encoding='utf-8-sig')
faltantes = [c for c in VARIAVEIS if c not in df.columns]
if faltantes:
    raise ValueError(f'Colunas não encontradas no CSV: {faltantes}')
for coluna in VARIAVEIS:
    df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
dados = df.dropna(subset=VARIAVEIS).copy()
if len(dados) < 30:
    raise ValueError('A base possui menos de 30 linhas completas para as variáveis escolhidas.')
registrar('CITIZENTECH — IPS BRASIL 2026')
registrar(f'Linhas originais: {len(df)}; linhas completas: {len(dados)}; colunas: {len(df.columns)}')
registrar('Fonte: arquivo IPS Brasil 2026 fornecido pelo usuário; unidade: município.')
registrar('Observação: os resultados são associações estatísticas, não efeitos causais.')

# 1. ESTATÍSTICAS DESCRITIVAS
registrar('\n1. ESTATÍSTICAS DESCRITIVAS')
descritivas = dados[VARIAVEIS].describe().T
registrar(descritivas.round(4).to_string())
descritivas.to_csv(SAIDA / 'estatisticas_descritivas.csv', encoding='utf-8-sig')

# 2. PROBABILIDADES NORMAIS (hipótese didática do enunciado)
registrar('\n2. DISTRIBUIÇÃO NORMAL — variável: ' + ACESSO)
x = dados[ACESSO]
mu, mediana, sigma = x.mean(), x.median(), x.std(ddof=0)
p_menor_media = stats.norm.cdf(mu, loc=mu, scale=sigma)
p_maior_mediana = stats.norm.sf(mediana, loc=mu, scale=sigma)
registrar(f'Média={mu:.4f}; mediana={mediana:.4f}; desvio padrão populacional={sigma:.4f}')
registrar(f'P(X < média) = {p_menor_media:.6f} ({p_menor_media*100:.2f}%)')
registrar(f'P(X > mediana) = {p_maior_mediana:.6f} ({p_maior_mediana*100:.2f}%)')
registrar('Ambos os eventos são possíveis, não certos nem impossíveis; probabilidades próximas a 50% indicam eventos aproximadamente equiprováveis ao complementar.')
registrar('A normalidade é assumida para o exercício, não comprovada pela amostra.')
plt.figure(figsize=(9, 5))
plt.hist(x, bins=35, density=True, color='steelblue', alpha=.45)
xs = np.linspace(x.min(), x.max(), 400)
plt.plot(xs, stats.norm.pdf(xs, mu, sigma), color='darkred', label='Normal teórica')
plt.axvline(mu, color='black', linestyle='--', label='Média')
plt.title('Distribuição do indicador de acesso à informação')
plt.xlabel(ACESSO); plt.ylabel('Densidade'); plt.legend()
figura('01_distribuicao_normal.png')

# 3. TESTES Z UNILATERAIS COM AMOSTRAS REPRODUTÍVEIS
# H0: média amostral compatível com mu0; H1: média < mu0 (a) / > mu0 (b).
# mu0 e sigma populacionais são calculados com os 5.570 municípios (referência didática).
registrar('\n3. TESTES DE HIPÓTESES Z (amostras aleatórias com sementes fixas)')
for rotulo, n, alpha, alternativa, semente in [
    ('a', 20, .06, 'menor', 202601), ('b', 25, .09, 'maior', 202602)
]:
    amostra = x.sample(n=n, random_state=semente)
    media_amostral = amostra.mean()
    z = (media_amostral - mu) / (sigma / np.sqrt(n))
    p = stats.norm.cdf(z) if alternativa == 'menor' else stats.norm.sf(z)
    critico = stats.norm.ppf(alpha) if alternativa == 'menor' else stats.norm.ppf(1-alpha)
    rejeita = p < alpha
    registrar(f'Caso {rotulo}: H0: μ={mu:.4f}; H1: μ {"<" if alternativa == "menor" else ">"} {mu:.4f}; n={n}; α={alpha:.2f}; σ={sigma:.4f}')
    registrar(f'Média amostral={media_amostral:.4f}; z={z:.4f}; z crítico={critico:.4f}; p={p:.6f}')
    registrar('Decisão: ' + ('rejeitar H0' if rejeita else 'não rejeitar H0'))
    registrar('A direção da média amostral é ' + ('compatível' if (media_amostral < mu if alternativa == 'menor' else media_amostral > mu) else 'oposta') + ' à hipótese alternativa.')
    amostra.to_csv(SAIDA / f'amostra_teste_{rotulo}.csv', index=False, encoding='utf-8-sig')
registrar('Nota metodológica: como a referência vem da própria base, os testes são demonstrações didáticas; não são inferência independente sobre outra população.')

# 4. BIVARIADA E REGRESSÃO LINEAR SIMPLES
registrar('\n4. ANÁLISE BIVARIADA')
a, b = dados[COBERTURA], dados[ACESSO]
cov = a.cov(b)
r, p_corr = stats.pearsonr(a, b)
registrar(f'Covariância amostral = {cov:.5f}; Pearson r = {r:.5f}; p-valor = {p_corr:.6g}')
registrar('Correlação ' + ('positiva' if r > 0 else 'negativa') + f', intensidade |r|={abs(r):.3f}.')
modelo_simples = sm.OLS(b, sm.add_constant(dados[[COBERTURA]])).fit()
resumo_modelo(modelo_simples, 'Regressão Simples')
plt.figure(figsize=(9, 6))
sns.regplot(data=dados, x=COBERTURA, y=ACESSO, scatter_kws={'alpha':.16, 's':10}, line_kws={'color':'darkred'})
plt.title('Dispersão e regressão linear simples')
figura('02_dispersao_regressao_simples.png')
plt.figure(figsize=(6, 5))
sns.heatmap(dados[[COBERTURA, ACESSO]].corr(), annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlação de Pearson — bivariada')
figura('03_correlacao_bivariada.png')
previsao_cobertura = float(a.median())
prev_simples = float(modelo_simples.predict(pd.DataFrame({'const':[1.0], COBERTURA:[previsao_cobertura]})).iloc[0])
registrar(f'Previsão: cobertura={previsao_cobertura:.2f} -> acesso previsto={prev_simples:.2f}')

# 5. MULTIVARIADA E REGRESSÃO LINEAR MÚLTIPLA
registrar('\n5. ANÁLISE MULTIVARIADA')
colunas_multi = [ACESSO, COBERTURA, BANDA, EDUCACAO]
mat_cov = dados[colunas_multi].cov()
mat_corr = dados[colunas_multi].corr()
mat_cov.to_csv(SAIDA / 'matriz_covariancia.csv', encoding='utf-8-sig')
mat_corr.to_csv(SAIDA / 'matriz_correlacao.csv', encoding='utf-8-sig')
registrar('Matriz de covariância:\n' + mat_cov.round(3).to_string())
registrar('Matriz de correlação:\n' + mat_corr.round(3).to_string())
registrar('Os sinais e magnitudes mostram como os indicadores variam conjuntamente; covariâncias dependem das unidades.')
# Amostra gráfica para legibilidade; matrizes e modelos usam a base completa.
visual = dados[colunas_multi].sample(n=min(700, len(dados)), random_state=42)
from pandas.plotting import scatter_matrix
axes = scatter_matrix(visual, figsize=(12, 12), alpha=.3, diagonal='hist', hist_kwds={'bins':25})
plt.suptitle('Dispersões multivariadas — amostra visual')
figura('04_dispersao_multivariada.png')
plt.figure(figsize=(9, 7))
sns.heatmap(mat_corr, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriz de correlação de Pearson — multivariada')
figura('05_correlacao_multivariada.png')
preditores_multi = [COBERTURA, BANDA, EDUCACAO]
modelo_multiplo = sm.OLS(dados[ACESSO], sm.add_constant(dados[preditores_multi])).fit()
resumo_modelo(modelo_multiplo, 'Regressão Múltipla')
entrada_multi = {col: float(dados[col].median()) for col in preditores_multi}
prev_multi = float(modelo_multiplo.predict(sm.add_constant(pd.DataFrame([entrada_multi]), has_constant='add')).iloc[0])
registrar(f'Previsão com 3 explicativas (medianas): {entrada_multi} -> acesso previsto={prev_multi:.2f}')

# 6. REGRESSÃO LOGÍSTICA BINÁRIA
# Classe observacional DERIVADA do indicador de acesso: 1 = valor >= mediana nacional.
# NÃO é um rótulo oficial nem um diagnóstico de exclusão digital.
registrar('\n6. REGRESSÃO LOGÍSTICA BINÁRIA')
limiar = float(dados[ACESSO].median())
dados['acesso_alto_relativo'] = (dados[ACESSO] >= limiar).astype(int)
features = [COBERTURA, BANDA, EDUCACAO]
X = dados[features]
y = dados['acesso_alto_relativo']
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=.25, random_state=42, stratify=y)
logit = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=42))
logit.fit(X_treino, y_treino)
predicoes = logit.predict(X_teste)
acuracia = accuracy_score(y_teste, predicoes)
matriz = confusion_matrix(y_teste, predicoes, labels=[0,1])
registrar(f'Classe 1: acesso >= mediana ({limiar:.4f}); classe 0: abaixo da mediana.')
registrar('Limiar definido pelo próprio conjunto de dados; rótulo analítico, não oficial.')
registrar(f'Treino: {len(X_treino)}; teste: {len(X_teste)}; acurácia no teste: {acuracia:.4f} ({acuracia*100:.2f}%)')
registrar('Matriz de confusão (linhas=real 0,1; colunas=previsto 0,1):\n' + str(matriz))
registrar(classification_report(y_teste, predicoes, digits=4, zero_division=0))
registrar('Interpretação: a diagonal indica acertos; os demais elementos indicam erros de classificação.')
intercepto = logit.named_steps['logisticregression'].intercept_[0]
coeficientes = logit.named_steps['logisticregression'].coef_[0]
registrar('Equação em variáveis padronizadas (z calculado pelas médias e desvios do treino):')
registrar('log(p/(1-p)) = ' + f'{intercepto:.6f}' + ''.join(f' + ({v:.6f}) × z[{c}]' for c,v in zip(features,coeficientes)))
registrar('p = 1 / (1 + exp(-logit)); classe prevista = 1 quando p >= 0,5.')
medias_treino = logit.named_steps['standardscaler'].mean_
escalas_treino = logit.named_steps['standardscaler'].scale_
pd.DataFrame({'variavel':features,'media_treino':medias_treino,'desvio_treino':escalas_treino,'coeficiente_padronizado':coeficientes}).to_csv(SAIDA/'coeficientes_logisticos.csv',index=False,encoding='utf-8-sig')
plt.figure(figsize=(6, 5))
sns.heatmap(matriz, annot=True, fmt='d', cmap='Blues', xticklabels=['Baixo','Alto'], yticklabels=['Baixo','Alto'])
plt.xlabel('Previsto'); plt.ylabel('Real'); plt.title('Matriz de confusão — conjunto de teste')
figura('06_matriz_confusao.png')
novo = pd.DataFrame([entrada_multi])
prob = float(logit.predict_proba(novo)[0,1])
classe = int(logit.predict(novo)[0])
registrar(f'Classificação com 3 explicativas (medianas): P(classe alta)={prob:.4f}; classe prevista={classe}')
registrar('Cuidado: o alvo é derivado do próprio indicador e os dados são transversais; não interpretar a classificação como causal ou como diagnóstico individual.')

dados.to_csv(SAIDA / 'base_analitica_com_classificacao.csv', index=False, encoding='utf-8-sig')
(SAIDA / 'resultados_estatisticos.txt').write_text('\n'.join(relatorio), encoding='utf-8')
registrar('\nFINALIZADO. Arquivos disponíveis na pasta resultados/.')
