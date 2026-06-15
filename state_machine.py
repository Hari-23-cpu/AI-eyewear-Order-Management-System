class OrderStateMachine:
    """Enforces absolute validity rules across operational workflow changes."""
    VALID_TRANSITIONS = {
        'PLACED': ['LAB_ROUTING'],
        'LAB_ROUTING': ['PROCESSING'],
        'PROCESSING': ['QC'],
        'QC': ['READY', 'PROCESSING'],  # QC failure loops back cleanly into processing
        'READY': ['DELIVERED'],
        'DELIVERED': []
    }

    @classmethod
    def can_transition(cls, current_status, next_status):
        return next_status in cls.VALID_TRANSITIONS.get(current_status, [])