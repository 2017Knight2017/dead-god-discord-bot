import discord
import re
from discord_components import DiscordComponents, Button, ButtonStyle
from discord.ext import commands
from json import loads

bot = commands.Bot(command_prefix="d!")
bot.remove_command("help")
language = "Русский"
info_number = 0


def func(string: str, items_list: list, entered_lang: str) -> str | tuple[str, str]:
    res = re.split(r"item:\[[A-Za-z0-9./\s\'\-!?]*]", string)
    string_items = re.findall(r"item:\[[A-Za-z0-9./\s\'\-!?]*]", string)
    for j, elem in enumerate(string_items):
        for i in items_list:
            if i["data-name"] == elem[6:-1]:
                match entered_lang:
                    case "Русский":
                        res.insert(j * 2 + 1, f'\"{i["data-name-rus"]}\"')
                    case "English":
                        res.insert(j * 2 + 1, f'\"{i["data-name"]}\"')
    if len(n := "\n\n".join(re.split(r"\n", "".join(res)))) > 4090:
        return n[:len(n)//2], n[len(n)//2:]
    else:
        return n


def func2(a: list) -> list:
    global language
    if language == "Русский":
        result = []
        for i in a:
            match i["value"]:
                case "treasure_room": result.append("Сокровищница")
                case "curse_room": result.append("Проклятая комната")
                case "shop": result.append("Магазин")
                case "devil_room": result.append("Комната дьявола")
                case "boss": result.append("Комната босса")
                case "angel_room": result.append("Комната ангела")
                case "library": result.append("Библиотека")
                case "secret_room": result.append("Секретная комната")
                case "planetarium": result.append("Планетарий")
                case "ultra_secret_room": result.append("Ультра секретная комната")
                case "golden_chest": result.append("Золотой сундук")
                case "wooden_chest": result.append("Деревянный сундук")
                case "red_chest": result.append("Красный сундук")
                case "baby_shop": result.append("Магазин малышей")
                case "old_chest": result.append("Старый сундук")
                case "moms_chest": result.append("Мамин сундук")
                case "beggar": result.append("Попрошайка")
                case "battery_bum": result.append("Заряженный попрошайка")
                case "devil_beggar": result.append("Дьявольский попрошайка")
                case "rotten_beggar": result.append("Гнилой попрошайка")
                case "key_master": result.append("Мастер ключей")
                case "crane_game": result.append("Автомат с краном")
                case "bomb_bum": result.append("Бомбовый попрошайка")
                case "greed_treasure_room": result.append("Сокровищница режима жадности")
                case "greed_secret_room": result.append("Секретная комната режима жадности")
                case "greed_curse_room": result.append("Проклятая комната режима жадности")
                case "greed_shop": result.append("Магазин режима жадности")
                case "greed_devil_room": result.append("Комната дьявола режима жадности")
                case "greed_boss": result.append("Комната босса режима жадности")
                case "greed_angel_room": result.append("Комната ангела режима жадности")
        return result
    return [i["label"] for i in a]


@bot.event
async def on_ready():
    print("Успешно зашёл")
    DiscordComponents(bot)


@bot.command(aliases=["h"])
async def help(ctx):
    """
    `d!help`: Выводит данное сообщение.
    """
    result = discord.Embed(title="Помощь по командам",
                           description="Аргумент в угловых скобках обязательный, а в квадратных — опциональный." +
                                       " Вместо полного написания команды можно использоватьего первую букву, например, `d!h` вместо `d!help`.")
    for key, elem in globals().items():
        if isinstance(elem, discord.ext.commands.Command):
            result.add_field(name=f"d!{key}", value=elem.help, inline=False)
    await ctx.send(embed=result)


@bot.command(aliases=["i"])
async def info(ctx, *item):
    """
    `d!info <item>`: Выдаёт информацию по указанному предмету.
    """
    global info_number
    info_number += 1
    local_info_number = info_number
    entered_item = " ".join(item)
    specific_item = {}
    with open("data.json", "r") as arr:
        arr = loads(arr.readline())
        for i, elem in enumerate(arr):
            match language:
                case "Русский":
                    if elem["data-name-rus"].lower() == entered_item.lower(): specific_item = arr[i]
                case "English":
                    if elem["data-name"].lower() == entered_item.lower(): specific_item = arr[i]
        result = discord.Embed(
            title=specific_item["data-name-rus"] if language == "Русский" else specific_item["data-name"],
            description=f"```{func(specific_item['data-description'], arr, language)}```")
        s = {"Доп. информация или синергии": specific_item['data-synergies'],
             "Баги": specific_item['data-bugs']}
        match loads(specific_item['data-type'])['label']:
            case "Пассивный":
                result.add_field(name="Тип", value="Пассивный предмет", inline=False)
                result.add_field(name="ID", value=specific_item['data-id'], inline=True)
                result.add_field(name="Качество", value=specific_item["data-quality"], inline=True)
                if loads(specific_item['data-pools'])[0]["label"] == "Без пула":
                    result.add_field(name="Пулы", value="Без пула", inline=False)
                else:
                    result.add_field(name="Пулы", value=', '.join(func2(loads(specific_item['data-pools']))),
                                     inline=False)
            case "Активный":
                result.add_field(name="Тип", value="Активный предмет", inline=False)
                result.add_field(name="ID", value=specific_item['data-id'], inline=True)
                result.add_field(name="Качество", value=specific_item["data-quality"], inline=True)
                result.add_field(name="Зарядов", value=specific_item["data-charges"] + " (Одноразовый)" * (
                            specific_item["data-charges"] == "0"), inline=True)
                if loads(specific_item['data-pools'])[0]["label"] == "Без пула":
                    result.add_field(name="Пулы", value="Без пула", inline=False)
                else:
                    result.add_field(name="Пулы", value=', '.join(func2(loads(specific_item['data-pools']))),
                                     inline=False)
                    s[func("Эффект от item:[Book of Virtues]", arr, language)] = specific_item["book-of-virtues-wisp"]
                    s[func("Эффект от item:[Birthright] Иуды", arr, language)] = specific_item['judas-birthright-effect']
            case "Брелок" | "Карты и Руны" | "Пилюли" as a:
                result.add_field(name="Тип", value=a, inline=True)
                result.add_field(name="ID", value=specific_item['data-id'], inline=True)
        try:
            if specific_item["data-opening"]:
                result.add_field(name="Как открыть", value=specific_item["data-opening"], inline=False)
            elif specific_item["data-opening-character"] == specific_item["data-opening-ending"] == "none":
                result.add_field(name="Как открыть", value="Открыто изначально", inline=False)
            else:
                result.add_field(name="Как открыть",
                                 value=f"Победить {specific_item['data-opening-ending']} за{' порченого' * (specific_item['character-type'] == 'tainted')} {specific_item['data-opening-character']}",
                                 inline=False)
        except KeyError: result.add_field(name="Как открыть", value="Открыто изначально", inline=False)
        result.set_thumbnail(url=specific_item["data-icon"])
        result.set_footer(text="Материал с сайта dead-god.ru")
        components = [Button(style=ButtonStyle.blue, label=i) for i in s.keys() if s[i]]
        if components:
            await ctx.send(embed=result, components=components)
            response = await bot.wait_for("button_click"), info_number
            desc = func(s[response[0].component.label], arr, language)
            if response[1] == local_info_number:
                if type(desc) == tuple:
                    await response[0].respond(embed=discord.Embed(
                        title=f"{response[0].component.label}:",
                        description=f"```{desc[0]}```"), components=[Button(style=ButtonStyle.blue, label="Читать далее")], ephemeral=False)
                    response = await bot.wait_for("button_click"), info_number
                    if response[0].component.label == "Читать далее":
                        await response[0].respond(embed=discord.Embed(description=f"```{desc[1]}```"), ephemeral=False)
                else:
                    await response[0].respond(embed=discord.Embed(description=f"```{desc}```"), ephemeral=False)
            else: pass
        else: await ctx.send(embed=result)


@bot.command(aliases=["l"])
async def lang(ctx, entered_lang=None):
    """
    `d!lang [language]`: Если параметр `language` не указан, то выводит текущий язык. Иначе меняет текущий язык на указанный.
    """
    global language
    if entered_lang is None:
        await ctx.send(f"Текущий язык названий предметов: {language}")
    match entered_lang.capitalize():
        case "Русский" | "English" as t:
            if language != t:
                language = t
                await ctx.send(f'Текущий язык названий предметов успешно установлен на {language}!')
            else:
                await ctx.send(f'Простите, текущий язык названий предметов уже был установлен на {language}.')
        case _:
            await ctx.send(f'Возможные значения для команды `d!lang`: `Русский` и `English`')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Простите, я не знаю такого предмета.' +
                       f' Попробуйте немного поменять его название и помните, что текущий язык предметов {language}.')
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Неизвестная команда. Чтобы посмотреть список всех команд, введите `d!help`.")


from f import TOKEN

bot.run(TOKEN)
