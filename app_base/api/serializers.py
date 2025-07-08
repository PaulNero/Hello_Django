from rest_framework import serializers

# serializers.Serializer – базовый класс, требующий ручного определения всех полей,  аналогично forms.Form. 
# Когда использовать:  
# • Для данных, не связанных напрямую с моделями Django (например, параметры  поиска, данные из внешних источников). 
# • Когда требуется очень специфичная структура выходных/входных данных,  сильно отличающаяся от модели. 
# • Для простых структур данных, где создание ModelSerializer избыточно. 

class DisplaySettingsSerializer (serializers.Serializer):
    theme = serializers.ChoiceField(choices=['light', 'dark'], default='light')
    items_per_page = serializers.IntegerField(min_value=5, max_value=50, default=10)
    show_avatars= serializers.BooleanField (default=True)
    last_updated = serializers.DateTimeField(read_only=True)    