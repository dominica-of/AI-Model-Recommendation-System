import pandas as pd
import psycopg2

def insert_models():
    conn = psycopg2.connect(
        dbname='model_metadata',
        user='dom',
        password='password',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Create table 
    cur.execute("""
    CREATE TABLE IF NOT EXISTS models (
        id SERIAL PRIMARY KEY,
        input_data TEXT,
        action TEXT,
        model_task TEXT,
        model TEXT,
        framework_library TEXT,
        github_stars FLOAT,
        normalized_github_stars FLOAT,
        citations FLOAT,
        normalized_citations FLOAT,
        open_source_proprietary TEXT,
        license TEXT,
        model_size_mb TEXT,
        model_size_normalized FLOAT,
        memory_requirement TEXT,
        memory_requirement_numeric FLOAT,
        memory_requirement_normalized FLOAT,
        hardware_accelerators TEXT,
        hardware_accelerators_normalized FLOAT,
        min_hardware_accelerators FLOAT,
        detailed_documentation TEXT,
        institution TEXT,
        institution_encoded FLOAT,
        url TEXT,
        paper_link TEXT,
        detailed_documentation_encoded INT,
        overall_score FLOAT,
        performance_score FLOAT,
        popularity_score FLOAT,
        licensing_score FLOAT,
        hardware_score FLOAT,
        documentation_score FLOAT,
        institution_score FLOAT
    );
    """)
    conn.commit()
    print("Table created")

    df = pd.read_csv('/Users/dom/Desktop/Thesis/thesis_root/data/prepropessed data/model_metadata_final.csv')

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO models (
                input_data, action, model_task, model, framework_library, github_stars,
                normalized_github_stars, citations, normalized_citations, open_source_proprietary,
                license, model_size_mb, model_size_normalized, memory_requirement,
                memory_requirement_numeric, memory_requirement_normalized, hardware_accelerators,
                hardware_accelerators_normalized, min_hardware_accelerators, detailed_documentation,
                institution, institution_encoded, url, paper_link, detailed_documentation_encoded,
                overall_score, performance_score, popularity_score, licensing_score,
                hardware_score, documentation_score, institution_score
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['Input Data'], row['Action'], row['Model Task'], row['Model'], row['Framework/Library'],
            row['Github stars'], row['Normalized Github stars'], row['Citations'], row['Normalized Citations'],
            row['Open Source/Proprietary'], row['License'], row['Model Size(MB)'], row['Model Size Normalized(MB)'],
            row['Memory Requirement(training)'], row['Memory Requirement Numeric'], row['Memory Requirement Normalized'],
            row['Hardware Accelerators'], row['Hardware Accelerators Normalized'], row['Minimum Hardware Accelerators'],
            row['Detailed Documentation'], row['Institution'], row['Institution Encoded'],
            row['URL'], row['Paper link'], row['Detailed Documentation Encoded'],
            row['Overall_Score'], row['Performance_Score'], row['Popularity_Score'], row['Licensing_Score'],
            row['Hardware_Score'], row['Documentation_Score'], row['Institution_Score']
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Data saved to PostgreSQL.")

if __name__ == '__main__':
    insert_models()
