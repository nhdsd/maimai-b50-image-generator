"""图像生成相关"""

from pathlib import Path
from typing import List, Union, Tuple

from PIL import Image, ImageDraw, ImageFont

from .models import ChartInfo, UserInfo
from .consts import (
    root, customdir, maimaidir, icondir, platedir, coverdir, HAN, TORUS, fcl, fsl, score_rank_l
)
from .api import MusicList
from .tools import dx_score, coloum_width, change_column_width, plate_finder
from .config import Config


# pylint: disable-next=too-few-public-methods
class DrawText:
    """Text drawing class"""
    def __init__(self, image: ImageDraw.ImageDraw, font: Path) -> None:
        self._img = image
        self._font = str(font)

    #pylint: disable-next=too-many-arguments, too-many-positional-arguments
    def draw(
        self,
        pos_x: int,
        pos_y: int,
        size: int,
        text: Union[str, int, float],
        color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        anchor: str = 'lt',
        stroke_width: int = 0,
        stroke_fill: Tuple[int, int, int, int] = (0, 0, 0, 0)
    ):
        """Main drawing function"""
        font = ImageFont.truetype(self._font, size)
        self._img.text( # type: ignore
            (pos_x, pos_y),
            str(text),
            color,
            font,
            anchor,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )


def music_picture(music_id: Union[int, str]) -> Path:
    """Get music illustration path"""
    music_id = int(music_id)
    if (_path := coverdir / f'{music_id}.png').exists():
        return _path
    if music_id > 100000:
        music_id -= 100000
        if (_path := coverdir / f'{music_id}.png').exists():
            return _path
    if 1000 < music_id < 10000 or 10000 < music_id <= 11000:
        for _id in (music_id + 10000, music_id - 10000):
            if (_path := coverdir / f'{_id}.png').exists():
                return _path
    return coverdir / '11000.png'

# pylint: disable-next=too-few-public-methods
class ScoreBaseImage:
    """Score base class"""
    _diff = [
        Image.open(maimaidir / 'b50_score_basic.png'),
        Image.open(maimaidir / 'b50_score_advanced.png'),
        Image.open(maimaidir / 'b50_score_expert.png'),
        Image.open(maimaidir / 'b50_score_master.png'),
        Image.open(maimaidir / 'b50_score_remaster.png')
    ]
    text_color = (124, 129, 255, 255)
    t_color = [
        (255, 255, 255, 255),
        (255, 255, 255, 255),
        (255, 255, 255, 255),
        (255, 255, 255, 255),
        (138, 0, 226, 255)
    ]
    id_color = [
        (129, 217, 85, 255),
        (245, 189, 21, 255),
        (255, 129, 141, 255),
        (159, 81, 220, 255),
        (138, 0, 226, 255)
    ]

    def __init__(self, image: Image.Image) -> None:
        self._im = image
        dr = ImageDraw.Draw(self._im)
        self._ha = DrawText(dr, HAN)
        self._to = DrawText(dr, TORUS)

    #pylint: disable-next=too-many-locals
    def whiledraw(
        self,
        data: List[ChartInfo],
        best: bool,
        music_list: MusicList,
        height: int = 0,
    ) -> None:
        """Main drawing function"""
        # y为第一排纵向坐标，dy为各行间距
        dy = 114
        x = 0
        if data:
            y = 235 if best else 1085
        else:
            y = height
        for num, info in enumerate(data):
            if num % 5 == 0:
                x = 16
                y += dy if num != 0 else 0
            else:
                x += 276

            cover = Image.open(music_picture(info.song_id)).resize((75, 75))
            version = Image.open(maimaidir / f'{info.type.upper()}.png').resize((37, 14))
            if info.rate.islower():
                rate = Image.open(
                    maimaidir / f'UI_TTR_Rank_{score_rank_l[info.rate]}.png'
                ).resize((63, 28))
            else:
                rate = Image.open(maimaidir / f'UI_TTR_Rank_{info.rate}.png').resize((63, 28))

            self._im.alpha_composite(self._diff[info.level_index], (x, y))
            self._im.alpha_composite(cover, (x + 12, y + 12))
            self._im.alpha_composite(version, (x + 51, y + 91))
            self._im.alpha_composite(rate, (x + 92, y + 78))
            if info.fc:
                fc = Image.open(
                    maimaidir / f'UI_MSS_MBase_Icon_{fcl[info.fc]}.png'
                ).resize((34, 34))
                self._im.alpha_composite(fc, (x + 154, y + 77))
            if info.fs:
                fs = Image.open(
                    maimaidir / f'UI_MSS_MBase_Icon_{fsl[info.fs]}.png'
                ).resize((34, 34))
                self._im.alpha_composite(fs, (x + 185, y + 77))

            dxscore = sum(music_list.by_id(str(info.song_id)).charts[info.level_index].notes) * 3
            dxnum = dx_score(info.dxScore / dxscore * 100)
            if dxnum:
                self._im.alpha_composite(
                    Image.open(
                        maimaidir / f'UI_GAM_Gauge_DXScoreIcon_0{dxnum}.png'
                    ).resize((47, 26)),
                    (x + 217, y + 80)
                )

            self._to.draw(
                x + 26,
                y + 98,
                13,
                info.song_id,
                self.id_color[info.level_index],
                anchor='mm'
            )
            title = info.title
            if coloum_width(title) > 18:
                title = change_column_width(title, 17) + '...'
            self._ha.draw(
                x + 93,
                y + 14,
                14,
                title,
                self.t_color[info.level_index],
                anchor='lm'
            )
            self._to.draw(
                x + 93,
                y + 38,
                30,
                f'{info.achievements:.4f}%', self.t_color[info.level_index],
                anchor='lm'
            )
            self._to.draw(
                x + 219,
                y + 65,
                15,
                f'{info.dxScore}/{dxscore}',
                self.t_color[info.level_index],
                anchor='mm'
            )
            self._to.draw(
                x + 93,
                y + 65,
                15,
                f'{info.ds} -> {info.ra}',
                self.t_color[info.level_index],
                anchor='lm'
            )

class DrawBest(ScoreBaseImage):
    """B50 drawing class"""
    def __init__(self, user_info: UserInfo) -> None:
        super().__init__(Image.open(maimaidir / 'b50_bg.png').convert('RGBA'))
        self.user_name = user_info.nickname
        self.plate = user_info.plate
        self.add_rating = user_info.additional_rating
        self.rating = user_info.rating
        self.sd_best = user_info.charts.sd
        self.dx_best = user_info.charts.dx

    def _find_rating_picture(self) -> str:
        if self.rating < 1000:
            num = '01'
        elif self.rating < 2000:
            num = '02'
        elif self.rating < 4000:
            num = '03'
        elif self.rating < 7000:
            num = '04'
        elif self.rating < 10000:
            num = '05'
        elif self.rating < 12000:
            num = '06'
        elif self.rating < 13000:
            num = '07'
        elif self.rating < 14000:
            num = '08'
        elif self.rating < 14500:
            num = '09'
        elif self.rating < 15000:
            num = '10'
        else:
            num = '11'
        return f'UI_CMN_DXRating_{num}.png'

    def _find_match_level_picture(self) -> str:
        if self.add_rating <= 10:
            num = f'{self.add_rating:02d}'
        else:
            num = f'{self.add_rating + 1:02d}'
        return f'UI_DNM_DaniPlate_{num}.png'

    # pylint: disable-next=too-many-locals, too-many-branches, too-many-statements
    async def draw(self, music_list_data: MusicList, config: dict[str, Config]) -> Image.Image:
        """Draw B50 async"""
        plate_name = config['plate']
        icon_name = config['icon']
        override = config['plate_override']

        logo = Image.open(maimaidir / 'logo.png').resize((249, 120))
        dx_rating = Image.open(maimaidir / self._find_rating_picture()).resize((186, 35))
        name = Image.open(maimaidir / 'Name.png')
        match_level = Image.open(maimaidir / self._find_match_level_picture()).resize((80, 32))
        class_level = Image.open(maimaidir / 'UI_FBR_Class_00.png').resize((90, 54))
        rating = Image.open(maimaidir / 'UI_CMN_Shougou_Rainbow.png').resize((270, 27))

        self._im.alpha_composite(logo, (14, 60))

        match plate_name:
            case int():
                try:
                    plate = Image.open(platedir / f'UI_Plate_{plate_name:06d}.png')
                except FileNotFoundError:
                    print(f"[WARNING]无法找到编号为{plate_name}的内置姓名框，将用默认姓名框代替。")
                    plate = Image.open(platedir / 'UI_Plate_000001.png')
            case str():
                try:
                    plate = Image.open(platedir / plate_name).convert("RGBA")
                except FileNotFoundError:
                    try:
                        plate = Image.open(root / plate_name).convert("RGBA")
                    except FileNotFoundError:
                        print(f"[WARNING]无法找到姓名框{plate_name}，将用默认姓名框代替。")
                        plate = Image.open(platedir / 'UI_Plate_300501.png')
                    else:
                        print("[WARNING]姓名框的加载位置已经更改。请参阅README。")
                else:
                    if (abs(130 * plate.size[0] - 800 * plate.size[1]) >
                        min(13 * plate.size[0], 80 * plate.size[1])):
                        print("[WARNING]姓名框成功加载，但与目标形状偏离过大，显示效果可能与预期不符。")
            case None:
                plate = Image.open(icondir / 'UI_Icon_000001.png')
        if self.plate and not override:
            plate = Image.open(platedir / f'UI_Plate_{plate_finder(self.plate)}.png')
            if plate_name is not None:
                print("[INFO]服务器上的牌子设置已覆盖姓名框设置。")
        plate = plate.resize((800, 130))
        self._im.alpha_composite(plate, (300, 60))

        match icon_name:
            case int():
                try:
                    icon = Image.open(icondir / f'UI_Icon_{icon_name:06d}.png')
                except FileNotFoundError:
                    print(f"[WARNING]无法找到编号为{icon_name}的内置头像，将用默认头像代替。")
                    icon = Image.open(icondir / 'UI_Icon_000001.png')
            case str():
                try:
                    icon = Image.open(customdir / f'{icon_name}.png').convert("RGBA")
                except FileNotFoundError:
                    try:
                        icon = Image.open(root / icon_name).convert("RGBA")
                    except FileNotFoundError:
                        print(f"[WARNING]无法找到头像{icon_name}，将用默认头像代替。")
                        icon = Image.open(icondir / 'UI_Icon_000001.png')
                    else:
                        print("[WARNING]头像的加载位置已经更改。请参阅README。")
                else:
                    if 10 * abs(icon.size[0] - icon.size[1]) > min(icon.size[0], icon.size[1]):
                        print("[WARNING]头像成功加载，但与目标形状偏离过大，显示效果可能与预期不符。")
            case None:
                icon = Image.open(icondir / 'UI_Icon_000001.png')
        icon = icon.resize((120, 120))
        self._im.alpha_composite(icon, (305, 65))
        self._im.alpha_composite(dx_rating, (435, 72))
        rating_value = f'{self.rating:05d}'
        for n, i in enumerate(rating_value):
            self._im.alpha_composite(
                Image.open(maimaidir / f'UI_NUM_Drating_{i}.png').resize((17, 20)),
                (520 + 15 * n, 80)
            )
        self._im.alpha_composite(name, (435, 115))
        self._im.alpha_composite(match_level, (625, 120))
        self._im.alpha_composite(class_level, (620, 60))
        self._im.alpha_composite(rating, (435, 160))

        self._ha.draw(445, 135, 25, self.user_name, (0, 0, 0, 255), 'lm')
        sdrating, dxrating = sum((_.ra for _ in self.sd_best)), sum((_.ra for _ in self.dx_best))
        self._to.draw(
            570, 172, 17,
            f'B35: {sdrating} + B15: {dxrating} = {self.rating}',
            (0, 0, 0, 255), 'mm', 3, (255, 255, 255, 255)
        )
        self._ha.draw(
            700, 1570, 27,
            'Designed by Yuri-YuzuChaN & BlueDeer233.',
            self.text_color, 'mm', 5, (255, 255, 255, 255)
        )

        self.whiledraw(self.sd_best, True, music_list_data)
        self.whiledraw(self.dx_best, False, music_list_data)

        return self._im
