#!/usr/bin/env python3
"""
Script untuk create table agents via Supabase client - Agent Makalah Backend
"""
from supabase import create_client, Client
from src.core.config import settings

def create_agents_table():
    """Create agents table via Supabase client"""
    print("🚀 Creating agents table via Supabase...")
    
    try:
        # Initialize Supabase client dengan service role key (admin privileges)
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_service_role_key  # Use service role for admin operations
        )
        
        # Create agents table via SQL
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS agents (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type VARCHAR(100) NOT NULL,
            status VARCHAR(50) DEFAULT 'active',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        """
        
        # Execute SQL via Supabase RPC
        response = supabase.rpc('exec_sql', {'sql': sql_create_table}).execute()
        
        print("✅ Agents table created successfully!")
        print(f"   - Response: {response}")
        
        # Insert sample data
        sample_agents = [
            {"name": "Agent-Makalah-Primary", "type": "research"},
            {"name": "Agent-Makalah-Secondary", "type": "writing"},
            {"name": "Agent-Makalah-Review", "type": "review"}
        ]
        
        insert_response = supabase.table("agents").insert(sample_agents).execute()
        print("✅ Sample agents inserted!")
        print(f"   - Inserted {len(insert_response.data)} agents")
        
        return True
        
    except Exception as e:
        print("❌ Failed to create agents table")
        print(f"   - Error: {str(e)}")
        return False

def test_agents_table():
    """Test agents table access"""
    print("\n🔍 Testing agents table access...")
    
    try:
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        
        # Test select from agents table
        response = supabase.table("agents").select("*").execute()
        
        print("✅ Agents table access successful!")
        print(f"   - Found {len(response.data)} agents")
        for agent in response.data:
            print(f"     • {agent['name']} ({agent['type']})")
        
        return True
        
    except Exception as e:
        print("❌ Failed to access agents table")
        print(f"   - Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎯 Agent-Makalah Database Setup\n")
    
    # Step 1: Create table
    table_created = create_agents_table()
    
    # Step 2: Test table access
    if table_created:
        test_agents_table()
    
    print("\n" + "="*50) 