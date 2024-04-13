from sqlalchemy import select
from database import TaskOrm, new_session
from schemas import TaskAdd, Task

class TaskRepository:
    @classmethod
    async def add_one(cls, data: TaskAdd) -> int:
        async with new_session() as session:
            task_dict = data.dict()
            task = TaskOrm(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[Task]:
        async with new_session() as session:
            query = select(TaskOrm)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks = [Task(id=task_model.id, name=task_model.name, description=task_model.description)
                     for task_model in task_models]
            return tasks
