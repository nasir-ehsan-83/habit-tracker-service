from typing import Tuple

def paginate(page: int = 1, limit: int = 10) -> Tuple[int, int]:
    # check that number of page should not be less than 1 or great than 10
    page = min(max(1, page), 10)
    
    # check that number of linit should not be less than 1 or great than 10
    limit = min(max(1, limit), 50)
    
    # calculate skip's value
    skip: int = (page - 1) * limit
        
    return skip, limit
