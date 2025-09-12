import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

VOICE_CHANNEL_ID = 847514073964740679

ADMIN_ROLE_ID = 946432769242845224

MEIBO_CHANNEL_ID = 847686946268512287

# 女性の場合: ja-JP-NanamiNeural, 男性の場合: ja-JP-KeitaNeural
VOICE_MODEL = "ja-JP-NanamiNeural"