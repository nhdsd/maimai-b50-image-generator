"""图像生成相关"""

from pathlib import Path
from typing import List, Optional, Union, Tuple
import asyncio

from PIL import Image, ImageDraw, ImageFont

from .models import ChartInfo, PlayInfoDefault, PlayInfoDev, UserInfo
from .consts import (
    root, maimaidir, platedir, coverdir, SIYUAN, TBFONT, fcl, fsl, score_rank_l
)
from .api import get_music_list
from .tools import dx_score, coloum_width, change_column_width

music_list = asyncio.run(get_music_list())
# pylint: disable-next=too-few-public-methods
class DrawText:
    """文字绘制类"""
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
        """绘图主方法"""
        font = ImageFont.truetype(self._font, size)
        self._img.text(
            (pos_x, pos_y),
            str(text),
            color,
            font,
            anchor,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill
        )


def music_picture(music_id: Union[int, str]) -> Path:
    """
    获取谱面图片路径

    Params:
        `music_id`: 谱面 ID
    Returns:
        `Path`
    """
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

class ScoreBaseImage:
    """基本分数绘制类"""
    _diff = [
        Image.open(maimaidir / 'b50_score_basic.png'),
        Image.open(maimaidir / 'b50_score_advanced.png'),
        Image.open(maimaidir / 'b50_score_expert.png'),
        Image.open(maimaidir / 'b50_score_master.png'),
        Image.open(maimaidir / 'b50_score_remaster.png')
    ]
    _rise = [
        Image.open(maimaidir / 'rise_score_basic.png'),
        Image.open(maimaidir / 'rise_score_advanced.png'),
        Image.open(maimaidir / 'rise_score_expert.png'),
        Image.open(maimaidir / 'rise_score_master.png'),
        Image.open(maimaidir / 'rise_score_remaster.png')
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
    bg_color = [
        (111, 212, 61, 255),
        (248, 183, 9, 255),
        (255, 129, 141, 255),
        (159, 81, 220, 255),
        (219, 170, 255, 255)
    ]
    id_diff = [Image.new('RGBA', (55, 10), color) for color in bg_color]

    title_bg = Image.open(maimaidir / 'title.png')
    title_lengthen_bg = Image.open(maimaidir / 'title-lengthen.png')
    design_bg = Image.open(maimaidir / 'design.png')
    aurora_bg = Image.open(maimaidir / 'aurora.png').convert('RGBA').resize((1400, 220))
    shines_bg = Image.open(maimaidir / 'bg_shines.png').convert('RGBA')
    pattern_bg = Image.open(maimaidir / 'pattern.png')
    rainbow_bg = Image.open(maimaidir / 'rainbow.png').convert('RGBA')
    rainbow_bottom_bg = Image.open(
        maimaidir / 'rainbow_bottom.png'
    ).convert('RGBA').resize((1200, 200))

    def __init__(self, image: Image.Image = None) -> None:
        self._im = image
        dr = ImageDraw.Draw(self._im)
        self._sy = DrawText(dr, SIYUAN)
        self._tb = DrawText(dr, TBFONT)

    #pylint: disable-next=too-many-locals
    def whiledraw(
        self,
        data: Union[List[ChartInfo], List[PlayInfoDefault], List[PlayInfoDev]],
        best: bool,
        height: int = 0
    ) -> None:
        """
        循环绘制成绩

        Params:
            `data`: 数据
            `dx`: 是否为新版本成绩
            `height`: 起始高度
        """
        # y为第一排纵向坐标，dy为各行间距
        dy = 114
        if data and isinstance(data[0], ChartInfo):
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

            self._tb.draw(
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
            self._sy.draw(
                x + 93,
                y + 14,
                14,
                title,
                self.t_color[info.level_index],
                anchor='lm'
            )
            self._tb.draw(
                x + 93,
                y + 38,
                30,
                f'{info.achievements:.4f}%', self.t_color[info.level_index],
                anchor='lm'
            )
            self._tb.draw(
                x + 219,
                y + 65,
                15,
                f'{info.dxScore}/{dxscore}',
                self.t_color[info.level_index],
                anchor='mm'
            )
            self._tb.draw(
                x + 93,
                y + 65,
                15,
                f'{info.ds} -> {info.ra}',
                self.t_color[info.level_index],
                anchor='lm'
            )


class DrawBest(ScoreBaseImage):
    """B50 绘制类"""
    def __init__(self, user_info: UserInfo) -> None:
        super().__init__(Image.open(maimaidir / 'b50_bg.png').convert('RGBA'))
        self.user_name = user_info.nickname
        self.plate = user_info.plate
        self.add_rating = user_info.additional_rating
        self.rating = user_info.rating
        self.sd_best = user_info.charts.sd
        self.dx_best = user_info.charts.dx

    def _find_rating_picture(self) -> str:
        """
        寻找指定的Rating图片

        Returns:
            `str` 返回图片名称
        """
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
        """
        寻找匹配等级图片

        Returns:
            `str` 返回图片名称
        """
        if self.add_rating <= 10:
            num = f'{self.add_rating:02d}'
        else:
            num = f'{self.add_rating + 1:02d}'
        return f'UI_DNM_DaniPlate_{num}.png'

    # pylint: disable-next=too-many-locals, too-many-branches, too-many-statements
    async def draw(
            self,
            icon_name: Optional[str] = None,
            plate_name: Optional[str] = None
        ) -> Image.Image:
        """异步绘制"""
        logo = Image.open(maimaidir / 'logo.png').resize((249, 120))
        dx_rating = Image.open(maimaidir / self._find_rating_picture()).resize((186, 35))
        name = Image.open(maimaidir / 'Name.png')
        match_level = Image.open(maimaidir / self._find_match_level_picture()).resize((80, 32))
        class_level = Image.open(maimaidir / 'UI_FBR_Class_00.png').resize((90, 54))
        rating = Image.open(maimaidir / 'UI_CMN_Shougou_Rainbow.png').resize((270, 27))

        self._im.alpha_composite(logo, (14, 60))
        if self.plate:
            plate = Image.open(platedir / f'{self.plate}.png').resize((800, 130))
            if plate_name is not None:
                print("由于有牌子，姓名框设置已被覆盖。")
        else:
            try:
                plate = Image.open(root / plate_name).convert("RGBA")
            except FileNotFoundError:
                print(f"无法找到姓名框{plate_name}，将用默认姓名框代替。")
                plate = Image.open(maimaidir / 'UI_Plate_300501.png')
            else:
                if (abs(130*plate.size[0] - 800*plate.size[1]) >
                    min(13*plate.size[0],80*plate.size[1])):
                    print("姓名框成功加载，但与目标形状偏离过大，显示效果可能与预期不符。")
            finally:
                plate = plate.resize((800, 130))
        self._im.alpha_composite(plate, (300, 60))
        try:
            if icon_name is not None:
                icon = Image.open(root / icon_name).convert("RGBA")
            else:
                icon = Image.open(maimaidir / 'UI_Icon_309503.png')
        except FileNotFoundError:
            print(f"无法找到头像{icon_name}，将用默认头像代替。")
            icon = Image.open(maimaidir / 'UI_Icon_309503.png')
        else:
            if 10 * abs(icon.size[0] - icon.size[1]) > min(icon.size[0], icon.size[1]):
                print("头像成功加载，但与目标形状偏离过大，显示效果可能与预期不符。")
        finally:
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

        self._sy.draw(445, 135, 25, self.user_name, (0, 0, 0, 255), 'lm')
        sdrating, dxrating = sum((_.ra for _ in self.sd_best)), sum((_.ra for _ in self.dx_best))
        self._tb.draw(
            570, 172, 17,
            f'B35: {sdrating} + B15: {dxrating} = {self.rating}',
            (0, 0, 0, 255), 'mm', 3, (255, 255, 255, 255)
        )
        self._sy.draw(
            700, 1570, 27,
            'Designed by Yuri-YuzuChaN & BlueDeer233.',
            self.text_color, 'mm', 5, (255, 255, 255, 255)
        )

        self.whiledraw(self.sd_best, True)
        self.whiledraw(self.dx_best, False)

        return self._im
