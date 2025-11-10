from repository import Repository, get_repository, Task

class TestInMemoryTasksRepository:
    repository: Repository

    def test_get_all(self):
        repository = get_repository()

        expected_value = [
            Task(id=1,name="My first task", status=False), 
            Task(id=2,name="My second task",status=False), 
            Task(id=3,name="My third task", status=False)
        ]

        result = repository.get_all()

        assert expected_value == result
    
    def test_add(self):
        repository = get_repository()

        expected_value = [
            Task(id=1,name="My first task", status=False),
            Task(id=2,name="My second task",status=False), 
            Task(id=3,name="My third task", status=False),
            Task(id=4,name="My fourth task", status=True)
        ]

        repository.add(Task(id=4,name="My fourth task", status=True))
        result = repository.get_all()

        assert expected_value == result
    
    def test_get_by_id(self):
        repository = get_repository()

        expected_value = Task(id=3,name="My third task", status=False)

        result = repository.get_by_id(3)

        assert expected_value == result