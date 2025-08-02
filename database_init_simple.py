# database_init.py
"""
Database initialization and seeding script for WTF Platform
Simple version without external dependencies
"""

import sqlite3
import uuid
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample data for testing the platform"""
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
    
    conn.commit()
    conn.close()
    print("Sample data created successfully!")

if __name__ == "__main__":
    create_sample_data()
