class Deck:
    """牌堆数据模型类"""
    
    def __init__(self):
        self.cards = {}
        self.initialize_deck()
    
    def initialize_deck(self):
        """初始化一副牌（不考虑花色）"""
        # 普通牌: 3-10, J, Q, K, A, 2
        ordinary_cards = {
            '3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4, '10': 4,
            'J': 4, 'Q': 4, 'K': 4, 'A': 4, '2': 4
        }
        
        # 王牌
        joker_cards = {
            '小王': 1, '大王': 1
        }
        
        self.cards = {**ordinary_cards, **joker_cards}
    
    def get_remaining_cards(self):
        """获取剩余的牌"""
        return {card: count for card, count in self.cards.items() if count > 0}
    
    def get_total_remaining(self):
        """获取剩余牌总数"""
        return sum(self.cards.values())
    
    def play_card(self, card_str):
        """出一张牌"""
        if card_str in self.cards and self.cards[card_str] > 0:
            self.cards[card_str] -= 1
            return True
        return False
    
    def play_cards(self, card_list):
        """出多张牌"""
        # 先检查所有牌是否都可以出
        temp_counts = self.cards.copy()
        for card in card_list:
            if card not in temp_counts or temp_counts[card] <= 0:
                return False, f"无法出牌 {card}，可能牌已出完或不存在"
            temp_counts[card] -= 1
        
        # 如果所有牌都可以出，则实际出牌
        for card in card_list:
            self.cards[card] -= 1
        
        return True, "出牌成功"
    
    def reset(self):
        """重置牌堆"""
        self.initialize_deck()