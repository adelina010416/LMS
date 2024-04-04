from rest_framework import serializers

from materials.models import Lesson, Course


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', many=True)

    def get_lesson_count(self, obj):
        return obj.lesson_set.all().count()

    class Meta:
        model = Course
        fields = '__all__'
