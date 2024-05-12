class UserFacultyGroupInfo:
    """Stores information about a user's faculty group.

    Attributes:
        faculty_id (int): The unique identifier of the faculty.
        group_id (int): The unique identifier of the group.
        group_name (str): The name of the group.
        subgroup (int): The subgroup. Can be 1 or 2 or 0, if no subgroup is specified.
    """
    def __init__(
        self,
        faculty_id: int,
        group_id: int,
        group_name: str,
        subgroup: int,
    ):
        self.faculty_id = faculty_id
        self.group_id = group_id
        self.group_name = group_name
        self.subgroup = subgroup
