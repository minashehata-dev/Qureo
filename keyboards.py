from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_grade_keyboard() -> InlineKeyboardMarkup:
    """لوحة الصفحة الرئيسية واختيار الصف الدراسي مع زر الانضمام لمجموعة وزر الأدمن في الصدارة وزر Clear"""
    buttons = [
        [
            InlineKeyboardButton(text="👥 الانضمام إلى مجموعة 🔑", callback_data="btn_enter_sub_pass")
        ],
        [
            InlineKeyboardButton(text="🎓 الصف الأول الثانوي (مسار JavaScript)", callback_data="grade_1")
        ],
        [
            InlineKeyboardButton(text="🎓 الصف الثاني الثانوي (مسار Python / JS)", callback_data="grade_2")
        ],
        [
            InlineKeyboardButton(text="👑 لوحة تحكم الأدمن (Admin Dashboard) ⚡", callback_data="btn_admin_panel")
        ],
        [
            InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_subject_keyboard(grade: str = "grade_1") -> InlineKeyboardMarkup:
    """لوحة توجيه لدروس البرمجة في كيريو مع زر Clear"""
    buttons = [
        [
            InlineKeyboardButton(text="💻 متابعة حل دروس البرمجة في كيريو", callback_data="subject_programming")
        ],
        [
            InlineKeyboardButton(text="🔙 تغيير الصف الدراسي", callback_data="btn_change_grade"),
            InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_about_keyboard() -> InlineKeyboardMarkup:
    """زر الرجوع من صفحة معلومات المطور مع زر Clear"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 العودة للقائمة الرئيسية", callback_data="btn_main_menu"),
                InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
            ]
        ]
    )


def get_main_keyboard(
    is_logged_in: bool = False,
    is_solving: bool = False,
    grade: str = "grade_1",
    subject: str = "programming",
    is_admin: bool = False
) -> InlineKeyboardMarkup:
    """لوحة المفاتيح الرئيسية للبوت مع تخصيص الصف الأول والثاني ومعلومات المطور وزر مسح الشاشة (Clear)"""
    buttons = []

    if is_admin:
        buttons.append([
            InlineKeyboardButton(text="👑 لوحة تحكم الأدمن (Admin Dashboard)", callback_data="btn_admin_panel")
        ])

    if not is_logged_in:
        # إذا لم يكن مسجلاً: نبرز له زر الانضمام لمجموعة وزر تسجيل الدخول بحسابه الخاص
        buttons.append([
            InlineKeyboardButton(text="👥 الانضمام إلى مجموعة 🔑", callback_data="btn_enter_sub_pass")
        ])
        buttons.append([
            InlineKeyboardButton(text="🔑 تسجيل الدخول بحسابك الخاص", callback_data="btn_login")
        ])
        buttons.append([
            InlineKeyboardButton(text="🎓 تغيير الصف / المادة", callback_data="btn_change_grade"),
            InlineKeyboardButton(text="ℹ️ معلومات البوت", callback_data="btn_about_bot")
        ])
        buttons.append([
            InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
        ])
        return InlineKeyboardMarkup(inline_keyboard=buttons)


    # إذا كان مسجلاً للدخول بالفعل:
    if is_solving:
        buttons.append([
            InlineKeyboardButton(text="⏹️ إيقاف الحل التلقائي", callback_data="btn_stop_solve"),
            InlineKeyboardButton(text="📸 التقاط شاشة حية", callback_data="btn_screenshot")
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="⚡ بدء الحل التلقائي الفوري (فتح المتصفح)", callback_data="btn_start_solve")
        ])

    # اختيار المسار لطلاب الصف الثاني
    if grade != "grade_1":
        buttons.append([
            InlineKeyboardButton(text="📚 اختيار المسار (Python / JS)", callback_data="btn_select_course")
        ])

    # تقرير المستوى الحالي وتقدم الـ API والانضمام لمجموعة
    buttons.append([
        InlineKeyboardButton(text="📊 مستواي الحالي والـ API", callback_data="btn_account_status"),
        InlineKeyboardButton(text="👥 الانضمام لمجموعة 🔑", callback_data="btn_enter_sub_pass")
    ])

    # تبديل الحساب وزر مسح الشاشة
    buttons.append([
        InlineKeyboardButton(text="🔄 تبديل الحساب", callback_data="btn_login"),
        InlineKeyboardButton(text="🧹 مسح الشاشة وتسجيل الخروج (Clear)", callback_data="btn_clear_screen")
    ])

    # معلومات البوت وتغيير الصف
    buttons.append([
        InlineKeyboardButton(text="ℹ️ معلومات البوت", callback_data="btn_about_bot"),
        InlineKeyboardButton(text="🎓 تغيير الصف / المادة", callback_data="btn_change_grade")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_status_keyboard(current_chapter_id: int = None, current_chapter_name: str = "") -> InlineKeyboardMarkup:
    """لوحة التحكم الخاصة بعرض حالة المستوى وتفاصيل الـ API"""
    buttons = []
    if current_chapter_id:
        btn_label = f"⚡ حل المستوى الحالي ({current_chapter_name})" if current_chapter_name else "⚡ حل هذا المستوى فوراً"
        buttons.append([
            InlineKeyboardButton(text=btn_label, callback_data=f"solve_chap_{current_chapter_id}")
        ])
    buttons.append([
        InlineKeyboardButton(text="🚀 حل جميع الفصول المتبقية", callback_data="btn_start_solve")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔄 تحديث", callback_data="btn_account_status"),
        InlineKeyboardButton(text="🔙 القائمة الرئيسية", callback_data="btn_main_menu")
    ])
    buttons.append([
        InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_courses_keyboard() -> InlineKeyboardMarkup:
    """لوحة اختيار المسار الدراسي في كيريو"""
    buttons = [
        [
            InlineKeyboardButton(
                text="⚡ مسار جافاسكريبت (JavaScript)",
                callback_data="course_js"
            )
        ],
        [
            InlineKeyboardButton(
                text="🐍 مسار بايثون (Python)",
                callback_data="course_python"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔗 إدخال رابط أو كود مستوى (مثال: 90032)",
                callback_data="course_custom"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 العودة للقائمة الرئيسية",
                callback_data="btn_main_menu"
            ),
            InlineKeyboardButton(
                text="🧹 مسح الشاشة (Clear)",
                callback_data="btn_clear_screen"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_solving_controls() -> InlineKeyboardMarkup:
    """أزرار التحكم أثناء تشغيل الحل"""
    buttons = [
        [
            InlineKeyboardButton(text="📸 لقطة شاشة الآن", callback_data="btn_screenshot"),
            InlineKeyboardButton(text="⏹️ إيقاف الحل", callback_data="btn_stop_solve")
        ],
        [
            InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """زر الإلغاء السريع ومسح الشاشة"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ إلغاء", callback_data="btn_cancel"),
                InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
            ]
        ]
    )


def get_chapters_keyboard(
    chapters: list,
    page: int = 1,
    per_page: int = 5,
    course_code: str = "py",
    completed_ids: set = None,
    current_chap_id: int = None
) -> InlineKeyboardMarkup:
    """لوحة مفاتيح تفاعلية لعرض مستويات وفصول المسار مع التنقل والصفحات"""
    if completed_ids is None:
        completed_ids = set()

    import math
    total_pages = max(1, math.ceil(len(chapters) / per_page))
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_chapters = chapters[start_idx:end_idx]

    buttons = []

    # إذا وجد مستوى حالي لم يكتمل، نظهر زر بارز لحله فوراً
    if current_chap_id:
        curr_obj = next((c for c in chapters if c.get("id") == current_chap_id), None)
        curr_name = curr_obj.get("name", "") if curr_obj else ""
        btn_text = f"🎯 المستوى الحالي: {curr_name} (حل مباشر)" if curr_name else "🎯 حل المستوى الحالي فوراً"
        buttons.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"sc_{current_chap_id}")
        ])

    # أزرار الفصول (زر لكل فصل)
    for c in page_chapters:
        cid = c.get("id")
        seq = c.get("seq", "?")
        name = c.get("name", f"فصل {seq}")
        q_cnt = c.get("question_count", 0)

        if cid in completed_ids:
            icon = "💎"
            status_text = "5/5"
        elif cid == current_chap_id:
            icon = "⏳"
            status_text = "حالي"
        else:
            icon = "📖"
            status_text = f"{q_cnt}س" if q_cnt else ""

        label = f"{icon} {seq}. {name} [{status_text}]"
        # عند الضغط يفتح أسئلة هذا الفصل سؤال بسؤال
        buttons.append([
            InlineKeyboardButton(text=label, callback_data=f"vc_{cid}")
        ])

    # سطر التنقل بين الصفحات
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️ السابق", callback_data=f"cp_{page-1}_{course_code}"))
        nav_row.append(InlineKeyboardButton(text=f"📄 {page} / {total_pages}", callback_data="noop"))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="التالي ➡️", callback_data=f"cp_{page+1}_{course_code}"))
        buttons.append(nav_row)

    # سطر الحل الجماعي التلقائي
    buttons.append([
        InlineKeyboardButton(text="⚡ حل جميع الفصول المتبقية تلقائياً", callback_data="btn_start_solve")
    ])

    # سطر التنقل الرئيسي
    buttons.append([
        InlineKeyboardButton(text="🔄 تحديث", callback_data=f"cp_{page}_{course_code}"),
        InlineKeyboardButton(text="🔙 تغيير المسار", callback_data="btn_select_course"),
        InlineKeyboardButton(text="🏠 الرئيسية", callback_data="btn_main_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_chapter_questions_keyboard(
    chapter_id: int,
    questions: list,
    test_type: str = "review",
    course_code: str = "py",
    solved_ids: set = None
) -> InlineKeyboardMarkup:
    """لوحة مفاتيح تفاعلية تعرض أسئلة الفصل ليختار المستخدم أي سؤال لحله بمفرده"""
    if solved_ids is None:
        solved_ids = set()

    buttons = []

    # سطر الأزرار لكل سؤال (زران في كل صف لترتيب الشاشة)
    q_buttons = []
    for idx, q_item in enumerate(questions, 1):
        q_info = q_item.get("question", q_item)
        qid = q_info.get("id") or q_item.get("id")
        q_type = q_info.get("type", "choice")
        type_label = "كود 💻" if q_type == "description" else "خيارات 🔘"

        status_icon = "✅" if qid in solved_ids else "❓"
        btn_label = f"{status_icon} س{idx} ({type_label})"

        q_buttons.append(
            InlineKeyboardButton(text=btn_label, callback_data=f"sq_{chapter_id}_{qid}")
        )

        if len(q_buttons) == 2:
            buttons.append(q_buttons)
            q_buttons = []

    if q_buttons:
        buttons.append(q_buttons)

    # زر حل الفصل كاملاً دفعة واحدة
    buttons.append([
        InlineKeyboardButton(text="⚡ حل هذا الفصل بالكامل (جميع الأسئلة)", callback_data=f"sc_{chapter_id}")
    ])

    # أزرار الرجوع
    buttons.append([
        InlineKeyboardButton(text="🔙 قائمة المستويات", callback_data=f"cp_1_{course_code}"),
        InlineKeyboardButton(text="🏠 الرئيسية", callback_data="btn_main_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_single_question_result_keyboard(
    chapter_id: int,
    next_q_id: int = None,
    course_code: str = "py"
) -> InlineKeyboardMarkup:
    """لوحة التحكم بعد حل سؤال مفرد في كيريو"""
    buttons = []
    if next_q_id:
        buttons.append([
            InlineKeyboardButton(text="⏩ حل السؤال التالي فوراً عبر الـ API", callback_data=f"sq_{chapter_id}_{next_q_id}")
        ])
    buttons.append([
        InlineKeyboardButton(text="📋 استعراض باقي أسئلة هذا المستوى", callback_data=f"vc_{chapter_id}"),
        InlineKeyboardButton(text="🔙 قائمة المستويات", callback_data=f"cp_1_{course_code}")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_links_bank_keyboard(
    chapters: list,
    page: int = 1,
    per_page: int = 5,
    course_code: str = "py"
) -> InlineKeyboardMarkup:
    """لوحة مفاتيح تفاعلية لبنك روابط الفصول مع عرض الروابط النظيفة وحالة كل مستوى"""
    import math
    total_pages = max(1, math.ceil(len(chapters) / per_page))
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    page_chapters = chapters[start_idx:end_idx]

    buttons = []

    # أزرار الفصول
    for c in page_chapters:
        cid = c.get("chapter_id") or c.get("id")
        seq = c.get("seq", "?")
        name = c.get("name", f"مستوى {seq}")
        completed = c.get("completed", 0)
        diamond = c.get("diamond", 0)

        if completed or diamond >= 5:
            icon = "💎"
            status = "مكتمل (5/5)"
        else:
            icon = "⏳"
            status = "غير مكتمل"

        label = f"{icon} {seq}. {name} [{status}]"
        buttons.append([
            InlineKeyboardButton(text=label, callback_data=f"sc_{cid}")
        ])

    # سطر التنقل بين الصفحات
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append(InlineKeyboardButton(text="⬅️ السابق", callback_data=f"lb_{page-1}_{course_code}"))
        nav_row.append(InlineKeyboardButton(text=f"📄 {page} / {total_pages}", callback_data="noop"))
        if page < total_pages:
            nav_row.append(InlineKeyboardButton(text="التالي ➡️", callback_data=f"lb_{page+1}_{course_code}"))
        buttons.append(nav_row)

    # زر استئناف الحل التلقائي
    buttons.append([
        InlineKeyboardButton(text="⚡ استئناف الحل التلقائي للمستويات المتبقية", callback_data="btn_start_solve")
    ])

    # العودة للرئيسية
    buttons.append([
        InlineKeyboardButton(text="🔄 تحديث", callback_data=f"lb_{page}_{course_code}"),
        InlineKeyboardButton(text="🏠 الرئيسية", callback_data="btn_main_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ==========================================
# لوحات المفاتيح لنظام الاشتراكات والأدمن
# ==========================================

def get_subscription_required_keyboard() -> InlineKeyboardMarkup:
    """لوحة تفعيل الاشتراك للمستخدم الجديد مع زر الانضمام لمجموعة ورابط المراسلة لحل المنصة كاملة"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👥 الانضمام إلى مجموعة 🔑", callback_data="btn_enter_sub_pass")
            ],
            [
                InlineKeyboardButton(text="💬 تواصل معنا لحل المنصة كاملة 🚀", url="https://m.me/1395840426948411")
            ],
            [
                InlineKeyboardButton(text="ℹ️ معلومات البوت", callback_data="btn_about_bot"),
                InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
            ]
        ]
    )


def get_admin_dashboard_keyboard() -> InlineKeyboardMarkup:
    """لوحة التحكم الرئيسية للأدمن (Admin Dashboard) مع خيار حل المستخدم العادي وكافة المميزات"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⚡ تصفح وحل فصول كيريو (حل مباشر مفتوح بالكامل) 🚀", callback_data="btn_select_course")
            ],
            [
                InlineKeyboardButton(text="📦 إنشاء باقة اشتراك جديدة (New Plan) ➕", callback_data="btn_admin_create_pkg"),
                InlineKeyboardButton(text="📋 إدارة باقات الاشتراك والمجموعات 👥", callback_data="btn_admin_list_pkgs")
            ],
            [
                InlineKeyboardButton(text="🎯 حل المنصة لحساب طالب خارجي بكود الطالب", callback_data="btn_admin_solve_account")
            ],
            [
                InlineKeyboardButton(text="🔒 إدارة كلمات مرور الأدمن (محمية)", callback_data="btn_admin_passwords"),
                InlineKeyboardButton(text="🔥 فحص ومزامنة فايربيس", callback_data="btn_admin_firebase_sync")
            ],
            [
                InlineKeyboardButton(text="🎓 تغيير الصف الدراسي (أولى / ثانية ثانوي)", callback_data="btn_change_grade"),
                InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
            ]
        ]
    )


def get_firebase_status_keyboard(is_connected: bool) -> InlineKeyboardMarkup:
    """أزرار فحص ومزامنة فايربيس السحابية"""
    buttons = []
    if is_connected:
        buttons.append([
            InlineKeyboardButton(text="🔄 مزامنة فورية لكافة البيانات لفايربيس", callback_data="btn_firebase_force_sync")
        ])
    else:
        buttons.append([
            InlineKeyboardButton(text="🔄 إعادة فحص وتحديث الاتصال الآن", callback_data="btn_admin_firebase_sync")
        ])
    buttons.append([
        InlineKeyboardButton(text="🔙 العودة للوحة الإدارة", callback_data="btn_admin_home")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_solve_grade_keyboard() -> InlineKeyboardMarkup:
    """لوحة اختيار الصف والمسار لحساب الطالب المراد حله من قبل الأدمن"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎓 الصف الأول الثانوي (مسار JavaScript ⚡)", callback_data="adm_solve_grade_1")
            ],
            [
                InlineKeyboardButton(text="🎓 الصف الثاني الثانوي (مسار Python 🐍)", callback_data="adm_solve_grade_2_py")
            ],
            [
                InlineKeyboardButton(text="🎓 الصف الثاني الثانوي (مسار JavaScript ⚡)", callback_data="adm_solve_grade_2_js")
            ],
            [
                InlineKeyboardButton(text="🔙 العودة للوحة الإدارة", callback_data="btn_admin_home")
            ]
        ]
    )


def get_plan_tiers_keyboard() -> InlineKeyboardMarkup:
    """لوحة اختيار نوع وخطة الباقة عند الإنشاء"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🥉 باقة 15 عميل (الأساسية)", callback_data="tier_15")
            ],
            [
                InlineKeyboardButton(text="🥈 الباقة الفضية (25 عميل)", callback_data="tier_25")
            ],
            [
                InlineKeyboardButton(text="🥇 الباقة الذهبية (40 عميل)", callback_data="tier_40")
            ],
            [
                InlineKeyboardButton(text="💎 الباقة الماسية (60 عميل)", callback_data="tier_60")
            ],
            [
                InlineKeyboardButton(text="⚙️ تحديد سعة مخصصة...", callback_data="tier_custom")
            ],
            [
                InlineKeyboardButton(text="🔙 العودة للوحة الإدارة", callback_data="btn_admin_home")
            ]
        ]
    )


def get_admin_groups_list_keyboard(groups: list) -> InlineKeyboardMarkup:
    """لوحة استعراض جميع الباقات المنشأة للأدمن"""
    buttons = []
    for g in groups:
        gid = g.get("group_id", "")
        tier = g.get("tier_name", "باقة")
        count = g.get("users_count", 0)
        max_u = g.get("max_users", 0)
        is_act = g.get("is_active", True)
        icon = "🟢" if is_act else "🔴"
        btn_text = f"{icon} {tier} ({count}/{max_u}) - [{gid}]"
        buttons.append([
            InlineKeyboardButton(text=btn_text, callback_data=f"view_pkg_{gid}")
        ])

    buttons.append([
        InlineKeyboardButton(text="➕ إنشاء باقة جديدة", callback_data="btn_admin_create_pkg")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 العودة للوحة الإدارة", callback_data="btn_admin_home")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_admin_group_detail_keyboard(group_id: str, is_active: bool) -> InlineKeyboardMarkup:
    """لوحة التحكم بباقة محددة مع خيار كشف الباسورد الآمن"""
    toggle_text = "⏸️ تعطيل الباقة مؤقتاً" if is_active else "▶️ إعادة تفعيل الباقة"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👁️ كشف باسورد الباقة (نافذة منبثقة آمنة)", callback_data=f"pkg_show_pass_{group_id}")
            ],
            [
                InlineKeyboardButton(text=toggle_text, callback_data=f"pkg_toggle_{group_id}"),
                InlineKeyboardButton(text="🗑️ حذف الباقة نهائياً", callback_data=f"pkg_delete_{group_id}")
            ],
            [
                InlineKeyboardButton(text="🔙 العودة لقائمة الباقات", callback_data="btn_admin_list_pkgs"),
                InlineKeyboardButton(text="🏠 لوحة الإدارة", callback_data="btn_admin_home")
            ]
        ]
    )


def get_admin_passwords_keyboard(passwords: list) -> InlineKeyboardMarkup:
    """لوحة استعراض وإدارة كلمات مرور الأدمن مع إخفاء وتشفير الباسورد عن الشاشة"""
    buttons = []
    for idx, p in enumerate(passwords):
        del_btn = [InlineKeyboardButton(text=f"🔒 كلمة مرور أدمن #{idx+1} (••••••••)", callback_data=f"show_adm_pass_{idx}")]
        if len(passwords) > 1:
            del_btn.append(InlineKeyboardButton(text="🗑️ مسح", callback_data=f"del_adm_pass_{idx}"))
        buttons.append(del_btn)

    buttons.append([
        InlineKeyboardButton(text="➕ إضافة كلمة مرور أدمن جديدة", callback_data="btn_add_adm_pass")
    ])
    buttons.append([
        InlineKeyboardButton(text="🔙 العودة للوحة الإدارة", callback_data="btn_admin_home")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_post_solve_completed_keyboard() -> InlineKeyboardMarkup:
    """لوحة الانتقال المباشر لقسم المستخدم بعد اكتمال الحل بنجاح"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👤 مستواي الحالي وبيانات الحساب (User Status)", callback_data="btn_account_status")
            ],
            [
                InlineKeyboardButton(text="⚡ حل فصول إضافية (Turbo API)", callback_data="btn_start_solve"),
                InlineKeyboardButton(text="🔄 تبديل الحساب", callback_data="btn_login")
            ],
            [
                InlineKeyboardButton(text="🏠 القائمة الرئيسية", callback_data="btn_main_menu"),
                InlineKeyboardButton(text="🧹 مسح الشاشة (Clear)", callback_data="btn_clear_screen")
            ]
        ]
    )

def get_contact_for_full_platform_keyboard() -> InlineKeyboardMarkup:
    """لوحة توجيه للمستخدم بعد إكمال أول 4 مستويات للتواصل مع الصفحة لحل المنصة كاملة مع زر الانضمام لمجموعة"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 الانضمام إلى مجموعة 🔑",
                    callback_data="btn_enter_sub_pass"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 تواصل معنا لحل المنصة كاملة 🚀",
                    url="https://m.me/1395840426948411"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏠 القائمة الرئيسية",
                    callback_data="btn_main_menu"
                ),
                InlineKeyboardButton(
                    text="🧹 مسح الشاشة (Clear)",
                    callback_data="btn_clear_screen"
                )
            ]
        ]
    )

