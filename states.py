from aiogram.fsm.state import State, StatesGroup


class UserStates(StatesGroup):
    # مرحلة اختيار الصف الدراسي والمادة
    waiting_for_grade = State()
    waiting_for_subject = State()

    # حالات تسجيل الدخول
    waiting_for_username = State()
    waiting_for_password = State()

    # إعدادات مفتاح Gemini
    waiting_for_gemini_key = State()

    # اختيار المسار أو المستوى
    waiting_for_custom_url = State()
    waiting_for_level_number = State()

    # حالة التشغيل الفعلي
    is_solving = State()

    # حالات الاشتراكات والأدمن
    waiting_for_admin_password = State()
    waiting_for_sub_password = State()
    admin_waiting_group_tier = State()
    admin_waiting_custom_limit = State()
    admin_waiting_group_id = State()
    admin_waiting_group_password = State()
    admin_waiting_new_admin_pass = State()
    admin_waiting_target_username = State()
    admin_waiting_target_password = State()
