import zipfile
from pathlib import Path
from PIL import Image

def extract_and_compress_images(zip_path: str, extract_dir: str, target_quality: int = 60):
    """
    ZIPファイルを解凍し、含まれる画像ファイルを極限まで軽量化する

    :param zip_path: 解凍するZIPファイルのパス
    :param extract_dir: 解凍先のフォルダパス
    :param target_quality: JPEGの保存品質（0〜100、低いほど軽量・低画質）
    """
    zip_file = Path(zip_path)
    extract_path = Path(extract_dir)

    # 1. ZIPファイルの解凍
    print(f"[{zip_file.name}] を解凍中...")
    with zipfile.ZipFile(zip_file, 'r') as zf:
        zf.extractall(extract_path)
    print("解凍が完了しました。画像の軽量化を開始します...")

    # 対応する画像拡張子の定義
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
    
    # 2. 解凍したフォルダ内の全ファイルを再帰的に検索
    for file_path in extract_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            try:
                # 画像を開く
                img = Image.open(file_path)
                
                # 透過PNGなどをJPEGで保存するためにRGBモードに変換
                if img.mode in ("RGBA", "P", "LA"):
                    img = img.convert("RGB")
                
                # 拡張子を強制的に .jpg に変更して上書き保存
                new_file_path = file_path.with_suffix('.jpg')
                
                # 極限まで軽くするための保存設定（qualityを下げ、optimizeを有効化）
                img.save(new_file_path, "JPEG", quality=target_quality, optimize=True)
                
                print(f"圧縮完了: {new_file_path.name}")
                
                # 元のファイルがJPG以外だった場合、圧縮前の元ファイルを削除
                if file_path != new_file_path:
                    file_path.unlink()

            except Exception as e:
                print(f"エラー発生 ({file_path.name}): {e}")

    print("すべての処理が完了しました。")

# ==========================================
# 実行部分
# ==========================================
if __name__ == "__main__":
    # 対象のZIPファイルのパスを指定
    ZIP_FILE_PATH = "定跡次の一手　立石流四間飛車（将棋世界2016年10月号付録）.zip" 
    
    # 解凍先のフォルダパスを指定
    EXTRACT_DIR = "./extracted_images"
    
    # スクリプトの実行
    # quality=10〜15あたりが実用性をギリギリ保った極限の軽さになります
    extract_and_compress_images(ZIP_FILE_PATH, EXTRACT_DIR, target_quality=15)