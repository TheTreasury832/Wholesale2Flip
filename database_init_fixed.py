# database_init_simple.py
"""
Database initialization script for WTF Platform
This should be run once to set up the database, not as the main app
"""

import sqlite3
import uuid
from datetime import datetime

def create_tables():
    """Create all required tables"""
    conn = sqlite3.connect('wtf_platform.db')
    cursor = conn.cursor()
    
    # Create buyers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buyers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            property_types TEXT,
            min_price REAL,
            max_price REAL,
            states TEXT,
            cities TEXT,
            deal_types TEXT,
            verified BOOLEAN DEFAULT 0,
            proof_of_funds BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Tables created successfully!")

def create_sample_data():
    """Create sample data for testing the platform"""
    # First ensure tables exist
    create_tables()
    
    conn = sqlite3.connect('wtf_platform.db')
    cursor = conn.cursor()
    
    # Sample buyers
    sample_buyers = [
        ('John Smith', 'john.smith@investor.com', '(555) 123-4567', 'single_family,multi_family', 
         100000, 300000, 'TX,OK', 'Dallas,Houston,Austin', 'cash,creative', 1, 1),
        ('Sarah Johnson', 'sarah@realtyinvest.com', '(555) 234-5678', 'single_family,condo',
         150000, 400000, 'TX,AR', 'Dallas,Fort Worth', 'cash', 1, 1),
        ('Mike Davis', 'mike.davis@properties.com', '(555) 345-6789', 'multi_family',
         200000, 500000, 'TX', 'Dallas', 'cash,subject_to', 1, 0),
        ('Lisa Wilson', 'lisa@buyhold.com', '(555) 456-7890', 'single_family',
         75000, 200000, 'TX,LA', 'Dallas,San Antonio', 'creative', 0, 0),
        ('Robert Chen', 'robert@fastcash.com', '(555) 567-8901', 'single_family,townhouse',
         120000, 350000, 'TX,NM', 'Austin,El Paso', 'cash', 1, 1),
    ]
    
    # Check if buyers already exist
    cursor.execute("SELECT COUNT(*) FROM buyers")
    if cursor.fetchone()[0] == 0:
        for buyer in sample_buyers:
            buyer_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO buyers (id, name, email, phone, property_types, min_price, max_price, 
                                  states, cities, deal_types, verified, proof_of_funds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (buyer_id,) + buyer)
        print(f"Added {len(sample_buyers)} sample buyers")
    else:
        print("Sample data already exists")
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    create_sample_data()
