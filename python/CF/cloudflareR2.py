from aiohttp import ClientResponse, ClientSession
from typing import Union, Optional, Any
import asyncio
import hydra
from omegaconf import OmegaConf, DictConfig
from .cloufflareError import CFError
import boto3


class CloudFlareR2():
    def __init__(self, _USERID: str, _BUCKET: str, _KEYID: str, _ACCESSKEY: str, _PUBLICURL: str) -> None:
        """__init__

        Args:
            _ENDPOINT (str): エンドポイント
            _KEYID (str): キーID
            _ACCESSKEY (str): アクセスキー
        """
        self.session = None # HTTPセッション
        self.USERID = _USERID
        self.BUCKET = _BUCKET
        self.KEYID = _KEYID # キーID
        self.ACCESSKEY = _ACCESSKEY # アクセスキー
        self.PUBLICURL = _PUBLICURL


        self.ENDPOINT = "https://" + self.USERID + ".r2.cloudflarestorage.com" # エンドポイント

        self.CLIENT = boto3.client(
            "s3",
            endpoint_url=self.ENDPOINT,
            aws_access_key_id=self.KEYID,
            aws_secret_access_key=self.ACCESSKEY,
        )
        pass

    async def __aenter__(self):
        """非同期処理開始
        """
        self.session = ClientSession() # セッションの立ち上げ
        await self.session.__aenter__() # 非同期セッションの開始
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """非同期終了処理
        """
        await self.session.__aexit__(exc_type, exc_val, exc_tb)

    async def _request(self, session:ClientSession, endpoint:str, method:str, data:Any):
        """HTTPリクエストを行う

        Args:
            session (ClientSession): HTTPセッション
            endpoint (str): エンドポイント
            method (str): HTTPメソッド
            data (Any): データ

        Returns:
            _type_: _description_
        """
        url = self.BASEURL + self.USERID + endpoint # HTTPエンドポイント作成
        # リクエストデータを作成する
        kwargs = {
            "headers" : self.headers,
            "data" : data
        }
        # HTTPリクエストを送信
        async with session.request(method, url, **kwargs) as rsp:
            return await self.treat_response(rsp, rsp)

    async def imageUploadfromFilePath(self, filePath:str) -> list[str]:
        with open(filePath, "rb") as img:
            data = {"file" : img}
            res = self._imageUpload(data)
            return res["result"]["variants"]

    async def _imageUpload(self, data: bytes):
        res = await self._request(self.session, "/images/v1", "POST", data)
        return res

    async def imageUpload(self, filename: str, data: bytes):
        """
        """

        self.CLIENT.upload_fileobj(
            data,
            self.BUCKET,
            filename,
        )

        urls: list[str] = []

        for _ in range(3):
            urls.append(self.PUBLICURL + "/" + filename)

        return urls

    @staticmethod
    async def treat_response(rsp: ClientResponse, data: Any) -> Any:
        """HTTPレスポンスを処理する

        Args:
            rsp (ClientResponse): レスポンスヘッダ
            data (Any): レスポンスデータ

        Returns:
            Any: パース後のデータ
        """
        # Json
        if rsp.content_type == "application/json":
            return await data.json()

        # Text
        if rsp.content_type == "text/plain" or rsp.content_type == "text/html":
            return await data.text()

        # Audio
        if rsp.content_type == "audio/mpeg" or rsp.content_type == "audio/webm":
            return await data.read()