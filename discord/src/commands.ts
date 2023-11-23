import { DiscordRequest } from "./utils";

interface choices {
  name: string,
  value: any,
}

interface CommandOption {
	type: number, // レスポンスタイプ
	name:  string, // オプション名
	description: string, // オプション説明
  choices?: Array<choices>,
	required?: boolean, // 必須かどうか
}

interface SetCommand {
	name: string, // コマンド名
	description: string, // コマンド説明
	options?: Array<CommandOption>, // オプション
	type: number, // レスポンスタイプ
}

interface Command {
  id: string,
  application_id: string,
  version: string,
  default_permission: boolean,
  default_member_permissions: any,
  type: Number,
  name: string,
  description: string,
  guild_id: string,
}

const sleep = waitTime => new Promise( resolve => setTimeout(resolve, waitTime) );

// ギルドコマンドを確認 (複数)
export async function HasGuildCommands(appId: string, guildId: string, commands: Array<SetCommand>) {
  if (guildId === '' || appId === '') return;
  commands.forEach((c: SetCommand) => HasGuildCommand(appId, guildId, c));
}

// ギルドコマンドの確認
async function HasGuildCommand(appId: string, guildId: string, command: SetCommand) {
	// ギルドコマンドAPIのエンドポイント
  const endpoint = `applications/${appId}/guilds/${guildId}/commands`;

  try {
		// インストール済みのコマンドリストの取得
    const res = await DiscordRequest(endpoint, { method: 'GET' });
    const data = await res.json();

    if (data) {
			// インストール済みのコマンド名の取得
      const installedNames = data.map((c) => c['name']);
			// 未インストールの場合インストールを行う
      //if (!installedNames.includes(command['name'])) {
      if (1) { // 常にインストール
        InstallGuildCommand(appId, guildId, command);
      } else {
      }
    }
  } catch (err) {
    console.error(err);
  }
}


function searchType(obj: Object){
  const type: any = Object.prototype.toString.call(obj);
  console.log(type);
}

export async function DeleteGuildCommandsAll(appId: string, guildId: string) {
  if (guildId === '' || appId === '') return;
  // 全コマンドを取得後、削除を行う
  const endpoint = `applications/${appId}/guilds/${guildId}/commands`; // コマンド用のエンドポイント作成
  const res = await DiscordRequest(endpoint, {method: "GET"}); // リクエストの送信
  const data = await res.json(); // パース
  data.forEach((c: Command) => DeleteGuildCommand(appId, guildId, c)) // 出力
  console.log("Commands Delete Completed")

}

async function DeleteGuildCommand(appId: string, guildId: string, commnad: any) {
  await sleep(1000);
  const commandId = commnad.id;
  let endpoint = `applications/${appId}/guilds/${guildId}/commands/`;
  const res = await DiscordRequest(endpoint + commandId, {method: "DELETE"});
}

// コマンドのインストール
export async function InstallGuildCommand(appId: string, guildId: string, command: SetCommand) {
  await sleep(1000);
  // ギルドコマンドAPIのエンドポイント
  const endpoint = `applications/${appId}/guilds/${guildId}/commands`;
  // コマンドのインストール
  try {
    await DiscordRequest(endpoint, { method: 'POST', body: command });
    console.log(`installed ${command.name}`);
  } catch (err) {
    console.error(err);
  }
}

// 起動チェック
export const CHECKWORK: SetCommand = {
  name: 'is_work',
  description: 'test discord bot response',
  type: 1,
};

// NAIAPIでの作成
export const NAIGENERATEIMAGE: SetCommand = {
  name: 'generate_image',
  description: 'NOVEALAIのAPIから画像生成する',
  options: [
    {
      type: 3,
      name: 'prompt',
      description: 'プロンプトを入力',
      required: true,
    }
  ],
  type: 1,
};

// オプション設定用コマンド
export const SETIMAGECONFIG: SetCommand = {
  name: 'set_image_config',
  description: '画像生成のオプションを設定する',
  options: [
    {
      type: 3,
      name: 'quality_toggle',
      description: 'クオリティスイッチ',
      choices: [
        {
            name: "True",
            value: "True",
        },
        {
            name: "False",
            value: "False",
        },
      ]
    },
    {
      type: 3,
      name: 'resolution',
      description: '画像サイズ',
      choices: [
        {
          name: "Wallpaper_Portrait",
          value: "Wallpaper_Portrait"
        },
        {
          name: "Wallpaper_Landscape",
          value: "Wallpaper_Landscape"
        },
        {
          name: "Small_Portrait",
          value: "Small_Portrait"
        },
        {
          name: "Small_Landscape",
          value: "Small_Landscape"
        },
        {
          name: "Small_Square",
          value: "Small_Square"
        },
        {
          name: "Normal_Portrait",
          value: "Normal_Portrait"
        },
        {
          name: "Normal_Landscape",
          value: "Normal_Landscape"
        },
        {
          name: "Normal_Square",
          value: "Normal_Square"
        },
        {
          name: "Small_Portrait_v2",
          value: "Small_Portrait_v2"
        },
        {
          name: "Small_Landscape_v2",
          value: "Small_Landscape_v2"
        },
        {
          name: "Small_Square_v2",
          value: "Small_Square_v2"
        },
        {
          name: "Normal_Portrait_v2",
          value: "Normal_Portrait_v2"
        },
        {
          name: "Normal_Landscape_v2",
          value: "Normal_Landscape_v2"
        },
        {
          name: "Normal_Square_v2",
          value: "Normal_Square_v2"
        },
        {
          name: "Small_Portrait_v3",
          value: "Small_Portrait_v3"
        },
        {
          name: "Small_Landscape_v3",
          value: "Small_Landscape_v3"
        },
        {
          name: "Small_Square_v3",
          value: "Small_Square_v3"
        },
        {
          name: "Normal_Portrait_v3",
          value: "Normal_Portrait_v3"
        },
        {
          name: "Normal_Landscape_v3",
          value: "Normal_Landscape_v3"
        },
        {
          name: "Normal_Square_v3",
          value: "Normal_Square_v3"
        }
      ]
    },
    {
      type: 3,
      name: 'sampler',
      description: 'サンプラー',
      choices: [
        {
          name: "k_lms",
          value: "k_lms"
        },
        {
          name: "k_euler",
          value: "k_euler"
        },
        {
          name: "k_euler_ancestral",
          value: "k_euler_ancestral"
        },
        {
          name: "k_heun",
          value: "k_heun"
        },
        {
          name: "plms",
          value: "plms"
        },
        {
          name: "ddim",
          value: "ddim"
        },
        {
          name: "nai_smea",
          value: "nai_smea"
        },
        {
          name: "nai_smea_dyn",
          value: "nai_smea_dyn"
        },
        {
          name: "k_dpmpp_2m",
          value: "k_dpmpp_2m"
        },
        {
          name: "k_dpmpp_2s_ancestral",
          value: "k_dpmpp_2s_ancestral"
        },
        {
          name: "k_dpmpp_sde",
          value: "k_dpmpp_sde"
        },
        {
          name: "k_dpm_2",
          value: "k_dpm_2"
        },
        {
          name: "k_dpm_2_ancestral",
          value: "k_dpm_2_ancestral"
        },
        {
          name: "k_dpm_adaptive",
          value: "k_dpm_adaptive"
        },
        {
          name: "k_dpm_fast",
          value: "k_dpm_fast"
        }
      ]
    },
    {
      type: 3,
      name: 'seed',
      description: 'シード',
    },
    {
      type: 3,
      name: 'scale',
      description: 'スケール',
    },
    {
      type: 3,
      name: 'steps',
      description: 'ステップ',
    },
    {
      type: 3,
      name: 'ucpreset',
      description: 'ネガティブプロンプトプリセット',
      choices: [
        {
          name: "Low_Quality_Bad_Anatomy(Curated, Full, Furry)",
          value: "Preset_Low_Quality_Bad_Anatomy"
        },
        {
          name: "Low_Quality(Curated, Full, Furry)",
          value: "Preset_Low_Quality"
        },
        {
          name: "Bad_Anatomy(Furry)",
          value: "Preset_Bad_Anatomy"
        },
        {
          name: "None(Curated, Full, Furry, v2, v3)",
          value: "Preset_None"
        },
        {
          name: "Heavy(v2, v3)",
          value: "Preset_Heavy"
        },
        {
          name: "Light(v2, v3)",
          value: "Presets_Light"
        }
      ]
    },
    {
      type: 3,
      name: 'uc',
      description: 'ネガティブプロンプト',
    },
    {
      type: 3,
      name: 'models',
      description: 'モデル',
      choices: [
        {
          name: "Anime_Curated",
          value: "Anime_Curated"
        },
        {
          name: "Furry",
          value: "Furry"
        },
        {
          name: "Anime_Full",
          value: "Anime_Full"
        },
        {
          name: "Anime_v2",
          value: "Anime_v2"
        },
        {
          name: "Anime_v3",
          value: "Anime_v3"
        }
      ]
    },
  ],
  type: 1,
};

// 設定をみる
export const SHOWIMAGESETTING: SetCommand = {
  name: 'show_image_setting',
  description: '画像設定の設定を見る',
  type: 1,
};
