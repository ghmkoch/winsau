import os
import progressbar
from enum import IntEnum

from textwrap import wrap

from task import TaskManager, TaskType


class _IParameterInput(object):
    def __init__(self, parameter): raise NotImplementedError()

    def get(self): raise NotImplementedError()


class _ParameterInputBase(_IParameterInput):
    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = self.parameter.filter(value)

    def __init__(self, parameter):
        self.parameter = parameter
        self._input = None


class _ParameterInputRawPrint(_ParameterInputBase):
    def get(self):
        parameter = self.parameter
        if parameter.label:
            print parameter.label
        self.input = raw_input('Insert value for "{}"{}:'.format(parameter.name, '(Default:{})'.format(
            parameter.default) if parameter.default else '')) or parameter.default
        return self.input


class ParameterInput(_IParameterInput):
    class Strategy(IntEnum):
        RAW_PRINT = 0

    def __init__(self, parameter, strategy=Strategy.RAW_PRINT):
        strategy_cls = {
            self.Strategy.RAW_PRINT: _ParameterInputRawPrint,
        }[strategy]
        self._strategy = strategy_cls(parameter)

    def get(self):
        return self._strategy.get()


class _IMainMenu(object):
    def show_loop(self):
        raise NotImplementedError()


class _MainMenuBase(_IMainMenu):
    def __init__(self):
        self.tasks = tuple(TaskManager.tasks_info((TaskType.ROOT, TaskType.USER)))


class _MainMenuTable(_MainMenuBase):
    MAX_COLUMNS = 80

    def __init__(self, cols=1, rows=5):
        super(_MainMenuTable, self).__init__()
        self.cols = cols
        self.rows = rows

    def _print_screen(self, msg=''):
        from colorclass import Color, Windows
        Windows.enable(auto_colors=True, reset_atexit=True)
        self._update_table()

        os.system('cls')
        print Color('{autobgblack}{autocyan}{}{/autocyan}{/autobgblack}').format(
            'List of tasks'.center(self.MAX_COLUMNS - 1))
        print b'\xc4'.decode('ibm437') * (self.MAX_COLUMNS - 1)
        print self._table.table
        print msg[:self.MAX_COLUMNS]
        input = raw_input("Select a task number or 'q' or 'quit' to quit:")
        Windows.disable()
        if input.lower() in ('quit', 'q', 'exit', 'e'):
            quit()
        else:
            os.system('cls')
            return input

    def _update_table(self):
        from terminaltables import SingleTable
        from colorclass import Color

        max_values = self.cols * self.rows
        col_out_width = int(self.MAX_COLUMNS / self.cols)
        col_inn_width = col_out_width - 3
        col0_inn_width = 2
        col1_inn_width = col_inn_width - col0_inn_width

        options_number = [' ' * col0_inn_width] * max_values
        options_label = [' ' * col1_inn_width] * max_values

        for pos, (name, description, steps) in enumerate(self.tasks):
            if pos <= max_values:
                label = [
                    Color('{autocyan}Name: {}{/autocyan}').format(name),
                    Color('{yellow}({} steps){/yellow}').format(steps),
                    "\n".join(wrap(description, col1_inn_width))
                ]

                wrapped_label = "\n".join(label)
                options_label[pos] = wrapped_label
                options_number[pos] = Color('{autowhite}{}{/autowhite}').format(str(pos))

        sliced = [None for i in range(self.cols * 2)]
        for col in range(self.cols):
            sliced[col * 2] = options_number[col * self.rows:col * self.rows + self.rows]
            sliced[1 + col * 2] = options_label[col * self.rows:col * self.rows + self.rows]

        table_data = zip(*sliced)

        table = SingleTable(table_data)
        table.inner_heading_row_border = False
        table.inner_row_border = True
        table.padding_left = 0
        table.padding_right = 0
        table.justify_columns = dict((i, 'left' if i % 2 else 'right') for i in range(self.cols * 2))

        self._table = table

    def show_loop(self):
        from colorclass import Color
        input = self._print_screen()



        while (int(input) > (len(self.tasks) - 1)) if input.isdigit() else True:
            input = self._print_screen(Color('{autored}INVALID INPUT "{}"{/autored}').format(input))
        TaskManager.run_by_name(self.tasks[int(input)][0])


class _MainMenuCurses(_MainMenuBase):
    pass


class MainMenu(_IMainMenu):
    class Strategy(IntEnum):
        TABLE = 0
        CURSES = 1

    def __init__(self, strategy=Strategy.TABLE):
        strategy_cls = {
            self.Strategy.TABLE: _MainMenuTable,
            self.Strategy.CURSES: _MainMenuCurses,
        }[strategy]
        self._strategy = strategy_cls()

    def show_loop(self):
        return self._strategy.show_loop()


class _IProcessDrawer(object):
    def __init__(self, task_name, steps_count):
        self.task_name = task_name
        self.steps_count = steps_count

    def update(self, step_cur, step_name, step_description):
        raise NotImplementedError()

    def finish(self):
        raise NotImplementedError()


class _ProcessDrawerBase(_IProcessDrawer):
    def __init__(self, task_name, steps_count):
        self.task_name = task_name
        self.steps_count = steps_count


class _ProcessDrawerPrintPlain(_ProcessDrawerBase):
    def __init__(self, task_name, steps_count):
        super(_ProcessDrawerPrintPlain, self).__init__(task_name, steps_count)
        print "Task {} starting".format(self.task_name)

    def update(self, step_cur, step_name, step_description):
        print '- Applying Step "{}.{}{}"({}/{})'.format(
            self.task_name,
            step_name,
            ":{}".format(step_description) if step_description else '',
            step_cur,
            self.steps_count,
        )

    def finish(self):
        print 'Task {} finished'.format(self.task_name)


class _ProcessDrawerProgressBar(_ProcessDrawerBase):
    def __init__(self, task_name, steps_count):
        super(_ProcessDrawerProgressBar, self).__init__(task_name, steps_count)
        self.bar = progressbar.ProgressBar(1, steps_count + 1)
        self._base_widget = ('Task "{}"'.format(self.task_name), progressbar.Bar(), progressbar.Percentage())

    def update(self, step_cur, step_name, step_description):
        widgets = self._base_widget + (
            ' Step "{}{}"({}/{})'.format(
                step_name,
                ":{}".format(step_description) if step_description else '',
                step_cur,
                self.steps_count,
            ),
            progressbar.ETA(),
        )

        self.bar.widgets = widgets
        self.bar.update(step_cur, True)

    def finish(self):
        widgets = self._base_widget + ('Done',)
        self.bar.widgets = widgets
        self.bar.finish()


class DrawProcess(_IProcessDrawer):
    class Strategy(IntEnum):
        PRINT_PLAIN = 0
        PROGRESS_BAR = 1

    def __init__(self, task_name, steps_count, strategy=Strategy.PRINT_PLAIN):
        strategy_cls = {
            self.Strategy.PRINT_PLAIN: _ProcessDrawerPrintPlain,
            self.Strategy.PROGRESS_BAR: _ProcessDrawerProgressBar,
        }[strategy]

        self._strategy = strategy_cls(task_name, steps_count)

    def update(self, step_cur, step_name, step_description):
        return self._strategy.update(step_cur, step_name, step_description)

    def finish(self):
        return self._strategy.finish()
