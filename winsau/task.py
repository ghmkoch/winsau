from enum import IntEnum
import logging

logger = logging.getLogger('task')


class TaskType(IntEnum):
    ROOT = 0
    FRAMEWORK = 1
    USER = 2


class _GenericSingleTask(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        return self._bound_func(*self.args, **self.kwargs)


class _TaskManagerType(type):
    _TASK_POOL = dict()
    _single_task_counter = 0

    def create_single_task(cls, func, *args, **kwargs):
        DinamicGenericSingleTask = type('DinamicGenericSingleTask{}'.format(cls._single_task_counter),
                                        (_GenericSingleTask,),
                                        {})
        DinamicGenericSingleTask.run = _GenericSingleTask.run
        DinamicGenericSingleTask.__dict__['run'].__dict__['_step_info'] = ('1', '')
        DinamicGenericSingleTask._bound_func = func

        task0 = Task(cls=DinamicGenericSingleTask, *args, **kwargs)
        cls._single_task_counter += 1
        return task0

    def register_task(cls, new_task):
        assert isinstance(new_task, Task)
        if new_task.name in cls._TASK_POOL:
            raise Exception('Duplicate task found: "{}"'.format(new_task.name))
        cls._TASK_POOL[new_task.name] = new_task

    def tasks_info(cls, allowed_types=tuple(TaskType)):
        for itask in cls._TASK_POOL.values():
            if itask._task_type in allowed_types:
                yield itask.name, itask.description, len(itask.get_steps())

    def run_by_name(cls, name, *args, **kwargs):
        return cls._TASK_POOL[name].execute(*args, **kwargs)

    def __getattr__(cls, key):
        if key in cls._TASK_POOL:
            return cls._TASK_POOL[key]


class TaskManager(object):
    __metaclass__ = _TaskManagerType


class TaskParameter(object):
    def __init__(self, name, label=None, default='', filter=str):
        self.name = name
        self.label = label
        self.default = default
        self.filter = filter


class Task(object):
    default_type = TaskType.ROOT

    def get_steps(self):
        steps = list()
        for name, method in self.cls.__dict__.iteritems():
            if hasattr(method, '_step_info'):
                step_name, step_description = method._step_info
                if step_name in [i[1] for i in steps]:
                    raise Exception('Duplicate steps found: "{}"'.format(step_name))
                steps.append([method.func_name, step_name, step_description])
        return tuple(steps)

    def __call__(self, *args, **kwargs):
        return self.execute(*args, **kwargs)

    def __init__(self, name, description, cls, parameters=[], config_data=None, task_type=default_type):
        self.name = name
        self.description = description
        self.cls = cls
        self.parameters = parameters
        self.config_data = config_data
        self._inputs = dict()
        self._task_type = task_type
        TaskManager.register_task(self)

    def _run_parameters(self):
        from tui import ParameterInput
        parameter_pool = self.parameters
        if isinstance(self.config_data, dict):
            if 'parameters' in self.config_data:
                try:
                    for parameter in self.config_data['parameters']:
                        parameter_pool += TaskParameter(**parameter)
                except:
                    raise Exception('Error loading parameters from configuration data')
        for parameter in parameter_pool:
            self._inputs[parameter.name] = ParameterInput(parameter).get()

    def execute(self, *override_args, **override_kwargs):
        from tui import DrawProcess
        steps = sorted(self.get_steps(), key=lambda k: k[1])
        if override_args or override_kwargs:
            taskobj = self.cls(*override_args, **override_kwargs)
        else:
            self._run_parameters()
            taskobj = self.cls(**self._inputs)
        if self._task_type == TaskType.FRAMEWORK:
            drawer = DrawProcess(self.name, len(steps), DrawProcess.Strategy.DUMMY)
        else:
            drawer = DrawProcess(self.name, len(steps))
        res = None
        for i, (func_name, step_name, step_description) in enumerate(steps):
            cur = i + 1
            drawer.update(cur, step_name, step_description)
            res = taskobj.__getattribute__(func_name)()
        drawer.finish()
        return res


# task decorator
def task(*args, **kwargs):
    def task_instance(cls):
        task0 = Task(cls=cls, *args, **kwargs)
        return cls

    return task_instance


# step decorator
def step(name, description=''):
    def step_func(func):
        func._step_info = (name, description)
        return func

    return step_func
