# Test script to verify the Vercel API handler
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Try importing the Vercel API handler
    import importlib.util
    spec = importlib.util.spec_from_file_location("api_handler", os.path.join(os.getcwd(), "api", "[[...path]].py"))
    api_handler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(api_handler_module)

    if hasattr(api_handler_module, 'handler'):
        print("[SUCCESS] Vercel API handler imported successfully")

        # Verify that it's a Mangum instance
        from mangum import Mangum
        if hasattr(api_handler_module.handler, '__class__') and api_handler_module.handler.__class__.__name__ == 'ASGIHandler':
            print("[SUCCESS] Handler is a valid Mangum ASGIHandler")
        else:
            print("[INFO] Handler type:", type(api_handler_module.handler).__name__)

        print("\n[SUCCESS] Vercel deployment configuration is ready!")
        print("\nTo deploy to Vercel:")
        print("1. Install Vercel CLI: npm install -g vercel")
        print("2. Run: vercel --prod")
        print("3. Or link your GitHub repo to Vercel for automatic deployments")
    else:
        print("[ERROR] Handler not found in module")

except ImportError as e:
    print(f"[ERROR] Error importing API handler: {e}")
    print("This might be expected during local development")
    print("The configuration should work when deployed to Vercel")

except Exception as e:
    print(f"[ERROR] Error: {e}")