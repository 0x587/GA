from pyecharts.faker import Faker
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType


def a() -> Line:
    key = Faker.choose()
    values = Faker.values()
    if len(key) != len(values):
        raise Warning('Keys do not match the length of values')
    current_data: list = values.copy()
    current_data[-1] = None
    current_line = (Line(init_opts=opts.InitOpts(theme=ThemeType.WONDERLAND))
                    .add_xaxis(key)
                    .add_yaxis('A', current_data, is_smooth=True, is_connect_nones=True,
                               # label_opts=opts.LabelOpts(is_show=False),
                               markpoint_opts=opts.MarkPointOpts(
                                   data=[opts.MarkPointItem(symbol=r'image://app/static/top.png',
                                                            symbol_size=60, type_='max'),
                                         opts.MarkPointItem(symbol=r'image://app/static/low.png',
                                                            symbol_size=40, type_='min')]
                               )))
    future_data: list = [None for _ in range(len(values))]
    future_data[-2:] = values[-2:]
    future_line = (Line()
                   .add_xaxis(key)
                   .add_yaxis('A', future_data, is_smooth=True, is_connect_nones=True,
                              linestyle_opts=opts.LineStyleOpts(type_="dashed"),
                              markpoint_opts=opts.MarkPointOpts(
                                  data=[opts.MarkPointItem(
                                      symbol='circle',
                                      name="下次预测", coord=[key[-1], values[-1]], value=values[-1])]
                              ),
                              ))
    current_line.set_global_opts(title_opts=opts.TitleOpts(title='历次成绩',
                                                           subtitle='预测结果使用{}次方程拟合'.
                                                           format('二')))
    return current_line.overlap(future_line)


a().render()
