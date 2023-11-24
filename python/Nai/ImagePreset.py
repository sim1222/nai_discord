from typing import TypedDict
import copy
import random
import math
from typing import Union, Any
import enum

class ImageSampler(enum.Enum):
    """サンプラー

    Args:
        enum (str): サンプラー
    """
    k_lms = "k_lms"
    k_euler = "k_euler"
    k_euler_ancestral = "k_euler_ancestral"
    k_heun = "k_heun"
    plms = "plms"  # doesn't work
    ddim = "ddim"

    nai_smea = "nai_smea"  # doesn't work
    nai_smea_dyn = "nai_smea_dyn"

    k_dpmpp_2m = "k_dpmpp_2m"
    k_dpmpp_2s_ancestral = "k_dpmpp_2s_ancestral"
    k_dpmpp_sde = "k_dpmpp_sde"
    k_dpm_2 = "k_dpm_2"
    k_dpm_2_ancestral = "k_dpm_2_ancestral"
    k_dpm_adaptive = "k_dpm_adaptive"
    k_dpm_fast = "k_dpm_fast"

class ImageModel(enum.Enum):
    """モデル

    Args:
        enum (str): モデル
    """
    Anime_Curated = "safe-diffusion" # デフォルト
    Furry = "nai-diffusion-furry" # ケモノ
    Anime_Full = "nai-diffusion" # v1?
    Anime_v2 = "nai-diffusion-v2" # v2
    Anime_v3 = "nai-diffusion-v3" # v3

class ImageResolution(enum.Enum):
    """画像サイズ

    Args:
        enum (tuple[int, int]): width, height
    """
    Wallpaper_Portrait = (1088, 1920)
    Wallpaper_Landscape = (1920, 1088)

    # v1
    Small_Portrait = (384, 640)
    Small_Landscape = (640, 384)
    Small_Square = (512, 512)

    Normal_Portrait = (512, 768)
    Normal_Landscape = (768, 512)
    Normal_Square = (640, 640)

    # v2
    Small_Portrait_v2 = (512, 768)
    Small_Landscape_v2 = (768, 512)
    Small_Square_v2 = (640, 640)

    Normal_Portrait_v2 = (832, 1216)
    Normal_Landscape_v2 = (1216, 832)
    Normal_Square_v2 = (1024, 1024)

    # v3
    Small_Portrait_v3 = (512, 768)
    Small_Landscape_v3 = (768, 512)
    Small_Square_v3 = (640, 640)

    Normal_Portrait_v3 = (832, 1216)
    Normal_Landscape_v3 = (1216, 832)
    Normal_Square_v3 = (1024, 1024)


class UCPreset(enum.Enum):
    """デフォルトネガティブワードプリセット

    Args:
        enum (int): プリセット操作
    """
    Preset_Low_Quality_Bad_Anatomy = 0
    Preset_Low_Quality = 1
    Preset_Bad_Anatomy = 2
    Preset_None = 3
    Preset_Heavy = 4
    Preset_Light = 5

class ImagePreset(TypedDict):
    """設定プリセット

    Args:
        TypedDict (_type_): プリセット一覧
    """
    quality_toggle: bool # クォリティup
    resolution: ImageResolution # 画像サイズ
    seed: int # シード値
    sampler: ImageSampler # サンプラー
    scale: Union[int, float] # 自由度
    steps: int # ステップ数
    n_samples: int # 絵数
    ucPreset: UCPreset # NAIデフォルトネガティブワード
    uc: str # ネガティブワード

_DEFUALT: ImagePreset = {
    "quality_toggle": True, # クォリティup
    "resolution": ImageResolution.Normal_Portrait, # 画像サイズ
    "seed": 0, # シード値
    "sampler": ImageSampler.k_euler_ancestral, # サンプラー
    "scale": 11, # 自由度
    "steps": 28, # ステップ数
    "n_samples": 1, # 絵数
    "ucPreset": UCPreset.Preset_Low_Quality_Bad_Anatomy,  # NAIデフォルトネガティブワード
    "uc": "" # ネガティブワード
}

_UCDEFAULT: dict = {
            UCPreset.Preset_Low_Quality_Bad_Anatomy: "nsfw, lowres, bad anatomy, bad hands, text, error, "
            "missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, "
            "jpeg artifacts, signature, watermark, username, blurry",
            UCPreset.Preset_Low_Quality: "nsfw, lowres, text, cropped, worst quality, low quality, normal quality, "
            "jpeg artifacts, signature, watermark, twitter username, blurry",
            UCPreset.Preset_Bad_Anatomy: None,
            UCPreset.Preset_None: "lowres",
            UCPreset.Preset_Heavy: "nsfw, lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, "
            "bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, "
            "artistic error, username, scan, [abstract]",
            UCPreset.Preset_Light: "nsfw, lowres, jpeg artifacts, worst quality, watermark, blurry, very displeasing",
    }

class ImagePreset():
    _DEFUALT: ImagePreset = {
        "quality_toggle": True, # クォリティup
        "resolution": ImageResolution.Normal_Portrait, # 画像サイズ
        "seed": 0, # シード値
        "sampler": ImageSampler.k_euler_ancestral, # サンプラー
        "scale": 11., # 自由度
        "steps": 28, # ステップ数
        "n_samples": 1, # 絵数
        "ucPreset": UCPreset.Preset_Low_Quality_Bad_Anatomy,  # NAIデフォルトネガティブワード
        "uc": "" # ネガティブワード
    }

    # デフォルトネガティブワード
    _UC_DEFAULT: dict = {
            UCPreset.Preset_Low_Quality_Bad_Anatomy: "nsfw, lowres, bad anatomy, bad hands, text, error, "
            "missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, "
            "jpeg artifacts, signature, watermark, username, blurry",
            UCPreset.Preset_Low_Quality: "nsfw, lowres, text, cropped, worst quality, low quality, normal quality, "
            "jpeg artifacts, signature, watermark, twitter username, blurry",
            UCPreset.Preset_Bad_Anatomy: None,
            UCPreset.Preset_None: "lowres",
            UCPreset.Preset_Heavy: "nsfw, lowres, {bad}, error, fewer, extra, missing, worst quality, jpeg artifacts, "
            "bad quality, watermark, unfinished, displeasing, chromatic aberration, signature, extra digits, "
            "artistic error, username, scan, [abstract]",
            UCPreset.Preset_Light: "nsfw, lowres, jpeg artifacts, worst quality, watermark, blurry, very displeasing",
    }

    _settings: dict[str, Any]

    def __init__(self, **kwargs):
        self._settings = copy.deepcopy(self._DEFUALT) # 完全コピー
        self.update(kwargs) # アップデート

    def __setitem__(self, o: str, v: Any):
        """キーアクセスの追加

        Args:
            o (str): key
            v (Any): value
        """
        # キーチェック
        assert o in self._DEFUALT, f"{o} is not a valid setting"
        # 型チェック
        assert isinstance(v, type(self._DEFUALT[o])) or isinstance(v, type(None)), f"Expected type [{type(self._DEFUALT[o])}], for [{o}] but got type [{type(v)}]"
        self._settings[o] = v # アップデート

    def update(self, values: dict[str, Any]):
        """設定のアップデート

        Args:
            values (dict[str, Any]): 辞書

        Returns:
            _type_: self
        """
        for k, v in values.items():
            self.__setitem__(k,v)
        return self

    def confirm(self):
        """設定の確定
        """
        settings = copy.deepcopy(self._settings)

        # 解像度
        resolution = settings.pop("resolution")
        if type(resolution) is ImageResolution:
            resolution = resolution.value
        settings["width"], settings["height"] = resolution

        # シード値
        if settings["seed"] == 0:
            settings["seed"] = random.randint(1, 0xFFFFFFFF)

        uc_preset: UCPreset = settings.pop("ucPreset")
        uc: str = settings.pop("uc")
        default_uc = self._UC_DEFAULT[uc_preset]
        combined_uc = f"{default_uc}, {uc}" if uc else default_uc
        settings["uc"] = combined_uc
        settings["ucPreset"] = uc_preset.value

        # サンプラー
        sampler: ImageSampler = settings.pop("sampler")
        settings["sampler"] = sampler.value

        return settings

    def calculate_cost(self):
        steps = self._settings["steps"]
        n_samples = self._settings["n_samples"]
        resolution = self._settings["resolution"]

        if type(resolution) is ImageResolution:
            resolution = resolution.value

        w, h = resolution

        r = w * h / 1024 / 1024
        per_step = (15.266497014243718 * math.exp(r * .6326248927474729) - 15.225164493059737) / 28
        per_sample = max(math.ceil(per_step * steps), 2)

        return per_sample * n_samples
