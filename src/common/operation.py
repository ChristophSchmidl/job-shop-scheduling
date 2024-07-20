class Operation:
    def __init__(self, id, job_id, machine_id, processing_time):
        self._id = id
        self._job_id = job_id # The job ID that the operation belongs to
        self._machine_id = machine_id # The machine id to execute the operation
        self._processing_time = processing_time # The original processing time of the operation
        self._start_time = None # When to start the operation on the given machine
        self._end_time = None # The time when the operation is finished on the given machine
        self._was_scheduled = False # Flag to indicate if the operation was scheduled

    @property
    def id(self) -> int:
        """Return the ID of the operation."""
        return self._id

    @property
    def job_id(self) -> int:
        """Return the ID of the job that the operation belongs to."""
        return self._job_id

    @property
    def machine_id(self) -> int:
        """Return the ID of the machine that processes the operation."""
        return self._machine_id
    
    @property
    def processing_time(self) -> int:
        """Return the processing time of the operation."""
        return self._processing_time
    
    @processing_time.setter
    def processing_time(self, processing_time: int) -> None:
        """Set the processing time of the operation."""
        self._processing_time = processing_time
    
    @property
    def start_time(self) -> int:
        """Return the scheduled start time of the operation."""
        return self._start_time
    
    @start_time.setter
    def start_time(self, start_time: int) -> None:
        """Set the scheduled start time of the operation."""
        self._start_time = start_time
    
    @property
    def end_time(self) -> int:
        """Return the scheduled end time of the operation."""
        return self._end_time
    
    @end_time.setter
    def end_time(self, end_time: int) -> None:
        """Set the scheduled end time of the operation."""
        self._end_time = end_time

    @property
    def was_scheduled(self) -> bool:
        """Return a boolean indicating if the operation was scheduled."""
        return self._was_scheduled
    
    @was_scheduled.setter
    def was_scheduled(self, was_scheduled: bool) -> None:
        """Set a boolean indicating if the operation was scheduled."""
        self._was_scheduled = was_scheduled

    def schedule(self, start_time: int) -> None:
        """ 
        When an operation is scheduled, a start time is set.
        The end time is the sum of the start and processing time.
        """
        self.start_time = start_time
        self.end_time = start_time + self.processing_time
        self.was_scheduled = True

    def reset(self) -> None:
        """
        Reset sets the operation to a state before it was scheduled.
        """
        self.start_time = None
        self.end_time = None
        self.was_scheduled = False

    def __str__(self):
        return f"Operation with job_id {self.job_id}, machine_id {self.machine_id}, processing_time {self.processing_time}, start_time {self.start_time}, end_time {self.end_time}"

    def __lt__(self, other):
        return self.start_time < other.start_time if self.start_time is not None and other.start_time is not None else False