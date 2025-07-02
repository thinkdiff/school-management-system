from pymongo import MongoClient
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
from src.config.settings import Settings

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """MongoDB database connection and operations"""
    
    _instance = None
    _client = None
    _database = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.settings = Settings()
            self._connect()
    
    def _connect(self):
        """Establish database connection"""
        try:
            config = self.settings.get_database_config()
            self._client = MongoClient(config['uri'])
            self._database = self._client[config['database']]
            
            # Test connection
            self._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    def get_database(self):
        """Get database instance"""
        return self._database
    
    def close_connection(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            logger.info("Database connection closed")

class BaseModel:
    """Base model class for database operations"""
    
    def __init__(self, collection_name: str):
        self.db_connection = DatabaseConnection()
        self.db = self.db_connection.get_database()
        self.collection = self.db[collection_name]
        self.collection_name = collection_name
    
    def create(self, data: Dict[str, Any]) -> str:
        """Create a new document"""
        try:
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()
            result = self.collection.insert_one(data)
            logger.info(f"Created document in {self.collection_name}: {result.inserted_id}")
            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Error creating document in {self.collection_name}: {str(e)}")
            raise
    
    def find_by_id(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Find document by ID"""
        try:
            from bson import ObjectId
            result = self.collection.find_one({'_id': ObjectId(document_id)})
            if result:
                result['_id'] = str(result['_id'])
            return result
        except Exception as e:
            logger.error(f"Error finding document by ID in {self.collection_name}: {str(e)}")
            return None
    
    def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find one document by query"""
        try:
            result = self.collection.find_one(query)
            if result:
                result['_id'] = str(result['_id'])
            return result
        except Exception as e:
            logger.error(f"Error finding document in {self.collection_name}: {str(e)}")
            return None
    
    def find_many(self, query: Dict[str, Any] = None, limit: int = None, skip: int = None, sort: List[tuple] = None) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        try:
            cursor = self.collection.find(query or {})
            
            if sort:
                cursor = cursor.sort(sort)
            if skip:
                cursor = cursor.skip(skip)
            if limit:
                cursor = cursor.limit(limit)
            
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])
                results.append(doc)
            
            return results
        except Exception as e:
            logger.error(f"Error finding documents in {self.collection_name}: {str(e)}")
            return []
    
    def update_by_id(self, document_id: str, data: Dict[str, Any]) -> bool:
        """Update document by ID"""
        try:
            from bson import ObjectId
            data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(
                {'_id': ObjectId(document_id)},
                {'$set': data}
            )
            success = result.modified_count > 0
            if success:
                logger.info(f"Updated document in {self.collection_name}: {document_id}")
            return success
        except Exception as e:
            logger.error(f"Error updating document in {self.collection_name}: {str(e)}")
            return False
    
    def update_one(self, query: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Update one document by query"""
        try:
            data['updated_at'] = datetime.utcnow()
            result = self.collection.update_one(query, {'$set': data})
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating document in {self.collection_name}: {str(e)}")
            return False
    
    def delete_by_id(self, document_id: str) -> bool:
        """Delete document by ID"""
        try:
            from bson import ObjectId
            result = self.collection.delete_one({'_id': ObjectId(document_id)})
            success = result.deleted_count > 0
            if success:
                logger.info(f"Deleted document from {self.collection_name}: {document_id}")
            return success
        except Exception as e:
            logger.error(f"Error deleting document from {self.collection_name}: {str(e)}")
            return False
    
    def delete_many(self, query: Dict[str, Any]) -> int:
        """Delete multiple documents"""
        try:
            result = self.collection.delete_many(query)
            logger.info(f"Deleted {result.deleted_count} documents from {self.collection_name}")
            return result.deleted_count
        except Exception as e:
            logger.error(f"Error deleting documents from {self.collection_name}: {str(e)}")
            return 0
    
    def count_documents(self, query: Dict[str, Any] = None) -> int:
        """Count documents matching query"""
        try:
            return self.collection.count_documents(query or {})
        except Exception as e:
            logger.error(f"Error counting documents in {self.collection_name}: {str(e)}")
            return 0
    
    def aggregate(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Perform aggregation query"""
        try:
            results = []
            for doc in self.collection.aggregate(pipeline):
                if '_id' in doc and doc['_id'] is not None:
                    doc['_id'] = str(doc['_id'])
                results.append(doc)
            return results
        except Exception as e:
            logger.error(f"Error in aggregation for {self.collection_name}: {str(e)}")
            return []