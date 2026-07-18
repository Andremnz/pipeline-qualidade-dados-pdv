import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Configuração de caminhos
pasta_script = Path(__file__).parent.resolve()
arquivo_entrada = pasta_script / "saida_financeiro.xlsx"
pasta_imagens = pasta_script / "imagens"
pasta_imagens.mkdir(exist_ok=True)
arquivo_saida = pasta_imagens / "curva_abc.png"

# Carrega os dados
if not arquivo_entrada.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {arquivo_entrada}. Execute o pipeline primeiro.")

df = pd.read_excel(arquivo_entrada)

# Seleciona os top 15 produtos para não poluir o gráfico
df_plot = df.head(15).copy()
df_plot['Nome Prod'] = df_plot['Nome Prod'].apply(lambda x: x[:28] + '..' if len(str(x)) > 28 else x)

# Configuração de estilo
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax1 = plt.subplots(figsize=(12, 6))

# Cores para cada classe ABC
cores_classe = {
    'A': '#2c3e50',  # Azul escuro / Slate
    'B': '#e67e22',  # Laranja
    'C': '#bdc3c7'   # Cinza claro
}
cores = df_plot['Classe_ABC'].map(cores_classe).fillna('#bdc3c7').tolist()

# Gráfico de barras (Faturamento)
bars = ax1.bar(df_plot['Nome Prod'], df_plot['Faturamento_Total'], color=cores, width=0.6, label='Faturamento')
ax1.set_ylabel('Faturamento (R$)', color='#2c3e50', fontweight='bold', fontsize=11)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R${x/1000:.0f}k'))
ax1.tick_params(axis='y', labelcolor='#2c3e50')
ax1.set_xticks(range(len(df_plot)))
ax1.set_xticklabels(df_plot['Nome Prod'], rotation=45, ha='right', fontsize=9)
ax1.grid(True, linestyle='--', alpha=0.5, axis='y')

# Segundo eixo y para a linha acumulada
ax2 = ax1.twinx()
ax2.plot(df_plot['Nome Prod'], df_plot['Part_Acum_%'], color='#e74c3c', marker='o', linewidth=2, label='Acumulado (%)')
ax2.set_ylabel('Participação Acumulada (%)', color='#e74c3c', fontweight='bold', fontsize=11)
ax2.tick_params(axis='y', labelcolor='#e74c3c')
ax2.set_ylim(0, 105)
ax2.grid(False)  # Evita grids conflitantes

# Adiciona marcas visuais de 80% e 95%
ax2.axhline(80, color='#e74c3c', linestyle=':', alpha=0.7)
ax2.axhline(95, color='#e74c3c', linestyle=':', alpha=0.5)

# Título
plt.title('Curva ABC de Vendas (Top 15 Produtos por Faturamento)', fontsize=13, fontweight='bold', pad=15)
fig.tight_layout()

# Salva o gráfico
plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
print(f"Gráfico Curva ABC salvo em: {arquivo_saida}")
