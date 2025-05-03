import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import altair as alt
    import marimo as mo
    import polars as pl

    return alt, mo, pl


@app.class_definition(hide_code=True)
class Container:
    def __init__(self, vol_init, frac_init):
        self.vol = vol_init
        # fraction of colored paint in container, rest is white
        self.frac = frac_init
        self.histo_vol = []
        self.histo_frac = []

    def snapshot(self):
        self.histo_vol.append(self.vol)
        self.histo_frac.append(self.frac)


@app.cell(hide_code=True)
def _(pl):
    class State:
        def __init__(self, vol_scoop, show=True, histo_all=False):
            self.left = Container(vol_init=1.0, frac_init=0.0)
            self.right = Container(vol_init=1.0, frac_init=1.0)
            self.vol_scoop = vol_scoop
            self.show = show
            self.histo_all = histo_all
            self.counter = 0
            self.snapshot()

            if self.show:
                self.display()

        def run(self, nb_2wy: int):
            for _ in range(nb_2wy):
                self.move_two_way()

        def move_two_way(self):
            self.move_one_way(direction="to_left")
            if self.show:
                self.display()
            self.move_one_way(direction="to_right")
            if self.show:
                self.display()

        def move_one_way(self, direction):
            if direction == "to_left":
                c_from = self.right
                c_to = self.left
            elif direction == "to_right":
                c_from = self.left
                c_to = self.right
            else:
                raise Exception("UNEXPECTED")

            self.counter += 1

            vol_to_new = c_to.vol + self.vol_scoop
            qty_to_cur = c_to.vol * c_to.frac
            qty_to_add = self.vol_scoop * c_from.frac
            frac_to_new = (qty_to_cur + qty_to_add) / vol_to_new

            c_to.vol = vol_to_new
            c_to.frac = frac_to_new

            c_from.vol = c_from.vol - self.vol_scoop
            c_from.frac = c_from.frac

            self.snapshot()

        def display(self):
            print(f"state: vol_scoop={self.vol_scoop}", end=" | ")
            print(
                f"volume: left={self.left.vol:.2f}, right={self.right.vol:.4f}",
                end=" | ",
            )
            print(f"fraction: left={self.left.frac:.2f}, right={self.right.frac:.4f}")

        def display_histo(self):
            print("histo left:")
            print(f"vol={self.left.histo_vol}")
            print(f"frac={self.left.histo_frac}")

            print("histo right:")
            print(f"vol =  {self.right.histo_vol}")
            print(f"frac = {self.right.histo_frac}")

        def snapshot(self):
            if self.counter % 2 == 0 or self.histo_all:
                self.left.snapshot()
                self.right.snapshot()

        def get_df_snapshot(self):
            n_histo = len(self.left.histo_vol)
            steps = list(range(n_histo))
            arr_df = []

            data = {
                "step": steps,
                "value": self.left.histo_vol,
                "type": ["left_vol"] * n_histo,
            }
            dfu = pl.DataFrame(data=data)
            arr_df.append(dfu)

            data = {
                "step": steps,
                "value": self.left.histo_frac,
                "type": ["left_frac"] * n_histo,
            }
            dfu = pl.DataFrame(data=data)
            arr_df.append(dfu)

            data = {
                "step": steps,
                "value": self.right.histo_vol,
                "type": ["right_vol"] * n_histo,
            }
            dfu = pl.DataFrame(data=data)
            arr_df.append(dfu)

            data = {
                "step": steps,
                "value": self.right.histo_frac,
                "type": ["right_frac"] * n_histo,
            }
            dfu = pl.DataFrame(data=data)
            arr_df.append(dfu)

            df = pl.concat(arr_df)
            return df

    return (State,)


@app.cell(hide_code=True)
def _():
    # s_test = State(vol_cup=0.15, show=True, histo_all=True)
    # for _ in range(3):
    #     s_test.move_two_way()
    # s_test.display_histo()

    return


@app.cell(hide_code=True)
def _(mo):
    slider_vol_scoop = mo.ui.slider(start=0.05, stop=0.95, step=0.05, value=0.25)
    return (slider_vol_scoop,)


@app.cell(hide_code=True)
def _(mo):
    slider_n_step = mo.ui.slider(start=0, stop=20, value=10)
    return (slider_n_step,)


@app.cell(hide_code=True)
def _(mo):
    toggle = mo.ui.checkbox(True)
    return (toggle,)


@app.cell(hide_code=True)
def _(State, mo, slider_n_step, slider_vol_scoop, toggle):
    s = State(vol_scoop=slider_vol_scoop.value, show=False, histo_all=toggle.value)
    s.run(nb_2wy=slider_n_step.value)

    mo.md(
        f"""
        ## How fast do color and white paints get mixed ?

        <img src="public/paint-pots.png" width="200" alt="missing img" />
        You have two 1-liter pots: the left contains white paint, the right contains colored paint.  
        Using a scoop of size s (<1 liter), you transfer s liters from right to left, mix, then transfer s liters back from left to right, and mix. This process is repeated multiple times; after each step, both pots have 1 liter of mixed paint.

        volume of scoop: {slider_vol_scoop}  
        number of steps: {slider_n_step}  
        show values mid-step: {toggle}
        """
    )
    return (s,)


@app.cell(hide_code=True)
def _(alt, df, mo):
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x="step",
            y="value",
            color="type",
        )
    )

    chart = mo.ui.altair_chart(chart)

    return (chart,)


@app.cell
def _(chart, mo):
    mo.vstack([chart])
    return


@app.cell(hide_code=True)
def _(s):
    df = s.get_df_snapshot()
    # df
    return (df,)


if __name__ == "__main__":
    app.run()
