#!/usr/bin/env python3
"""
Test script untuk koneksi Supabase - Agent Makalah Backend
"""
import asyncio
import asyncpg
from supabase import create_client, Client
from src.core.config import settings

def test_supabase_client():
    """Test Supabase client connection"""
    print("=== Testing Supabase Client Connection ===")
    try:
        # Initialize Supabase client
        supabase: Client = create_client(
            settings.supabase_url,
            settings.supabase_anon_key
        )
        
        # Test connection dengan simple health check
        response = supabase.table("_supabase_migrations").select("*").limit(1).execute()
        
        print("✅ Supabase Client Connection: SUCCESS")
        print(f"   - URL: {settings.supabase_url}")
        print(f"   - Project Ref: {settings.supabase_project_ref}")
        print(f"   - Response status: {response.count if hasattr(response, 'count') else 'Unknown'}")
        return True
        
    except Exception as e:
        print("❌ Supabase Client Connection: FAILED")
        print(f"   - Error: {str(e)}")
        return False

async def test_postgres_direct():
    """Test direct PostgreSQL connection"""
    print("\n=== Testing Direct PostgreSQL Connection ===")
    try:
        # Test direct connection ke PostgreSQL
        conn = await asyncpg.connect(settings.database_url)
        
        # Test simple query
        version = await conn.fetchval('SELECT version()')
        await conn.close()
        
        print("✅ Direct PostgreSQL Connection: SUCCESS")
        print(f"   - Host: {settings.postgres_host}")
        print(f"   - Database: {settings.postgres_db}")
        print(f"   - PostgreSQL Version: {version[:50]}...")
        return True
        
    except Exception as e:
        print("❌ Direct PostgreSQL Connection: FAILED")
        print(f"   - Error: {str(e)}")
        return False

async def test_database_structure():
    """Test database structure dan create table jika perlu"""
    print("\n=== Testing Database Structure ===")
    try:
        conn = await asyncpg.connect(settings.database_url)
        
        # Check jika table 'agents' ada
        table_exists = await conn.fetchval("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = 'agents'
            );
        """)
        
        if not table_exists:
            print("📝 Creating 'agents' table...")
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS agents (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    type VARCHAR(100) NOT NULL,
                    status VARCHAR(50) DEFAULT 'active',
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
            """)
            
            # Insert sample data
            await conn.execute("""
                INSERT INTO agents (name, type) VALUES 
                ('Agent-Makalah-Primary', 'research'),
                ('Agent-Makalah-Secondary', 'writing'),
                ('Agent-Makalah-Review', 'review')
                ON CONFLICT DO NOTHING;
            """)
            print("✅ Sample agents table created with test data")
        else:
            print("✅ Agents table already exists")
        
        # Count records
        count = await conn.fetchval("SELECT COUNT(*) FROM agents")
        print(f"   - Agents count: {count}")
        
        await conn.close()
        return True
        
    except Exception as e:
        print("❌ Database Structure Test: FAILED")
        print(f"   - Error: {str(e)}")
        return False

def test_credentials_validity():
    """Test kredensial Supabase"""
    print("\n=== Testing Supabase Credentials ===")
    
    credentials = {
        "URL": settings.supabase_url,
        "Project Ref": settings.supabase_project_ref,
        "Anon Key": settings.supabase_anon_key[:20] + "...",
        "Service Role Key": settings.supabase_service_role_key[:20] + "...",
        "Database URL": settings.database_url.replace(settings.postgres_password, "***"),
    }
    
    for key, value in credentials.items():
        print(f"   - {key}: {value}")
    
    print("✅ All credentials loaded from configuration")
    return True

async def main():
    """Main test function"""
    print("🚀 Agent-Makalah Supabase Connection Tests\n")
    
    # Test all components
    results = []
    
    # 1. Test credentials
    results.append(test_credentials_validity())
    
    # 2. Test Supabase client
    results.append(test_supabase_client())
    
    # 3. Test direct PostgreSQL
    results.append(await test_postgres_direct())
    
    # 4. Test database structure
    results.append(await test_database_structure())
    
    # Summary
    print("\n" + "="*50)
    print("🎯 TEST SUMMARY")
    print(f"✅ Passed: {sum(results)} / {len(results)}")
    print(f"❌ Failed: {len(results) - sum(results)} / {len(results)}")
    
    if all(results):
        print("\n🎉 ALL TESTS PASSED! Supabase ready untuk Agent-Makalah!")
    else:
        print("\n⚠️  Some tests failed. Check configuration dan credentials.")
    
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main()) 