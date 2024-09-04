from flask import Flask, jsonify, request, render_template, redirect, url_for
import logging
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration using environment variables, with defaults for local development
DATABASE = os.getenv('DATABASE', 'app_db')
USER = os.getenv('USER', 'postgres')
PASSWORD = os.getenv('PASSWORD', 'postgres')
HOST = os.getenv('HOST', 'localhost')
PORT = os.getenv('PORT', '5432')

# Establish database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(dbname=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        return conn
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return None

# Create the required table if it doesn't exist
def create_table():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS texts (
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL
                    );
                """)
                conn.commit()
                logger.info("Table 'texts' checked/created successfully.")
        except Exception as e:
            logger.error(f"Error creating table: {e}")
        finally:
            conn.close()

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, content FROM texts;")
                texts = cursor.fetchall()
                return render_template('index.html', texts=texts)
        except Exception as e:
            logger.error(f"Error fetching texts: {e}")
            return "Error loading page", 500
        finally:
            conn.close()
    else:
        return "Error connecting to the database", 500

@app.route('/add', methods=['POST'])
def add_text():
    content = request.form.get('content')
    if not content:
        return redirect(url_for('index'))

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO texts (content) VALUES (%s);", (content,))
                conn.commit()
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Error adding text: {e}")
            return "Error adding text", 500
        finally:
            conn.close()
    else:
        return "Error connecting to the database", 500

@app.route('/edit/<int:id>', methods=['POST'])
def edit_text(id):
    content = request.form.get('content')
    if not content:
        return redirect(url_for('index'))

    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE texts SET content = %s WHERE id = %s;", (content, id))
                conn.commit()
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Error updating text: {e}")
            return "Error updating text", 500
        finally:
            conn.close()
    else:
        return "Error connecting to the database", 500

@app.route('/delete/<int:id>', methods=['POST'])
def delete_text(id):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM texts WHERE id = %s;", (id,))
                conn.commit()
            return redirect(url_for('index'))
        except Exception as e:
            logger.error(f"Error deleting text: {e}")
            return "Error deleting text", 500
        finally:
            conn.close()
    else:
        return "Error connecting to the database", 500

@app.route('/liveness', methods=['GET'])
def liveness_probe():
    return jsonify({"status": "alive"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "healthy"}), 200
    else:
        return jsonify({"status": "unhealthy"}), 500

if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=80)
