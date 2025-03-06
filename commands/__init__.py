import os
import importlib

async def setup_commands(bot):
    command_files = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py") and f != "__init__.py"]

    for file in command_files:
        try:
            module = importlib.import_module(f"commands.{file}")
            print(f"{file} をロード中...")  
            await module.setup(bot)  
            print(f"{file} をロード完了")
        except Exception as e:
            print(f"{file} のロード中にエラー発生: {e}")