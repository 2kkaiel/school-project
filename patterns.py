from obstacle import ObstacleFactory

PATTERNS = {
    'SINGLE': '1개 장애물',
    'DOUBLE': '2개 연속 장애물, 간격 좁음',
    'TRIPLE': '3개 연속 장애물',
    'STAIRS_UP': '점점 높아지는 3개',
    'STAIRS_DOWN': '점점 낮아지는 3개',
    'WAVE': '높음-낮음-높음',
    'TUNNEL': '위아래 동시 배치, 중간 통과',
    'ZIGZAG': '좌우 교차 패턴',
    'RHYTHM': '일정 리듬으로 4개',
    'BOSS': '복잡한 조합 패턴'
}

class PatternGenerator:
    @staticmethod
    def get_pattern(pattern_name, x, speed):
        obstacles = []
        if pattern_name == 'SINGLE':
            obstacles.extend(ObstacleFactory.create_by_type('basic', x, speed))
        elif pattern_name == 'DOUBLE':
            obstacles.extend(ObstacleFactory.create_by_type('basic', x, speed))
            obstacles.extend(ObstacleFactory.create_by_type('basic', x + 150, speed))
        elif pattern_name == 'TRIPLE':
            obstacles.extend(ObstacleFactory.create_by_type('basic', x, speed))
            obstacles.extend(ObstacleFactory.create_by_type('basic', x + 150, speed))
            obstacles.extend(ObstacleFactory.create_by_type('basic', x + 300, speed))
        elif pattern_name == 'STAIRS_UP':
            obstacles.extend(ObstacleFactory.create_by_type('low', x, speed))
            obstacles.extend(ObstacleFactory.create_by_type('basic', x + 150, speed))
            obstacles.extend(ObstacleFactory.create_by_type('tall', x + 300, speed))
        
        # This is a placeholder for pattern width calculation
        pattern_width = 400 if pattern_name in ['TRIPLE', 'STAIRS_UP'] else 200 if pattern_name == 'DOUBLE' else 100

        return obstacles, pattern_width
