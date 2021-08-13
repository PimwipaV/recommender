from sqlalchemy import create_engine

def create_engine_load_data():
    '''Load data into memory and return an engine and data as a dataframe.'''
    # Load and fill database
    engine = create_engine('sqlite:///:memory:', echo=False)

    for f in os.listdir('data/movies'):
        if f[-4:] == '.csv':
            data = pd.read_csv(f'data/movies/{f}')
            data.to_sql(f[:-4], engine)
            print(f[:-4], 'loaded succesfully')

    # LOAD DATA
    query = 'SELECT "userId", ratings."movieId", movies.title, rating FROM ratings JOIN movies ON ratings."movieId" = movies."movieId";'
    all_ratings = pd.read_sql(query, engine)

    return engine, all_ratings