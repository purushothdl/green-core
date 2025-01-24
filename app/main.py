from fastapi import FastAPI
from app.routes import user_routes
from app.routes import org_routes
from app.routes import waste_routes
from app.routes import chat_routes
from app.core.error_handler import global_exception_handler
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Include routes
app.include_router(user_routes.router, prefix='/api')
app.include_router(org_routes.router, prefix='/api')
app.include_router(waste_routes.router, prefix='/api')
app.include_router(chat_routes.router, prefix='/api')

# Global exception handler
app.add_exception_handler(Exception, global_exception_handler)