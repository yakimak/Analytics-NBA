import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_player_data():
    try:
        df = pd.read_csv('Players.csv')
        # Конвертируем рост из см в метры для анализа
        df['height_m'] = df['height'] / 100
        # Рассчитываем BMI (индекс массы тела)
        df['bmi'] = df['weight'] / (df['height_m']**2)
        return df
    except FileNotFoundError:
        print("Файл Players.csv не найден")
        return None

def analyze_physical_stats(df):
    # Анализ физических характеристик
    physical_stats = df[['height', 'weight', 'bmi']].describe()
    
    # Топ-5 самых высоких игроков
    tallest = df.nlargest(5, 'height')[['Player', 'height']]
    
    # Топ-5 самых тяжелых игроков
    heaviest = df.nlargest(5, 'weight')[['Player', 'weight']]
    
    return physical_stats, tallest, heaviest

def plot_physical_distributions(df):
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    sns.histplot(data=df, x='height', bins=15)
    plt.title('Распределение роста игроков')
    
    plt.subplot(1, 3, 2)
    sns.histplot(data=df, x='weight', bins=15)
    plt.title('Распределение веса игроков')
    
    plt.subplot(1, 3, 3)
    sns.scatterplot(data=df, x='height', y='weight', hue='bmi')
    plt.title('Соотношение роста и веса')
    
    plt.tight_layout()
    plt.savefig('physical_stats.png')

def analyze_birthplaces(df):
    # Анализ мест рождения
    birth_state_counts = df['birth_state'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=birth_state_counts.values, y=birth_state_counts.index)
    plt.title('Топ-10 штатов по количеству игроков')
    plt.savefig('birth_states.png')
    
    return birth_state_counts

def main():
    player_data = load_player_data()
    if player_data is None:
        return
    
    # Анализ физических характеристик
    stats, tallest, heaviest = analyze_physical_stats(player_data)
    
    print("\nОбщая статистика физических показателей:")
    print(stats)
    
    print("\nТоп-5 самых высоких игроков:")
    print(tallest.to_string(index=False))
    
    print("\nТоп-5 самых тяжелых игроков:")
    print(heaviest.to_string(index=False))
    
    # Визуализация физических характеристик
    plot_physical_distributions(player_data)
    
    # Анализ мест рождения
    birth_stats = analyze_birthplaces(player_data)
    print("\nТоп-10 штатов по количеству игроков:")
    print(birth_stats)
    
    # Сохранение данных с новыми вычисленными полями
    player_data.to_csv('analyzed_players.csv', index=False)

if __name__ == "__main__":
    main()