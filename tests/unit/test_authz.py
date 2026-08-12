"""Aşama 18 birim testleri: yetki motoru (IDOR/BOLA parametre doğrulaması)."""

import unittest

from src.safety.authorization import (
    ALLOW,
    BLOCK_IDOR,
    REQUIRE_AUTHORIZATION,
    AccessRequest,
    Session,
    validate_access,
)


class OwnDataTests(unittest.TestCase):
    def test_student_own_grade(self) -> None:
        s = Session(role="ogrenci", user_id="u1", school_id="s1")
        r = AccessRequest(action="read_grade", student_id="u1")
        self.assertEqual(validate_access(r, s).decision, ALLOW)

    def test_student_other_grade_denied(self) -> None:
        s = Session(role="ogrenci", user_id="u1", school_id="s1")
        r = AccessRequest(action="read_grade", student_id="u2")
        self.assertEqual(validate_access(r, s).decision, REQUIRE_AUTHORIZATION)


class IdorTests(unittest.TestCase):
    def test_cross_school_blocked(self) -> None:
        s = Session(role="ogretmen", user_id="t1", school_id="s1")
        r = AccessRequest(action="read_grade", student_id="u9", school_id="s2")
        self.assertEqual(validate_access(r, s).decision, BLOCK_IDOR)

    def test_admin_cross_school_allowed(self) -> None:
        s = Session(role="admin", user_id="a1", school_id="s1")
        r = AccessRequest(action="read_grade", student_id="u9", school_id="s2")
        self.assertEqual(validate_access(r, s).decision, ALLOW)


class TeacherScopeTests(unittest.TestCase):
    def test_teacher_unauthorized_course(self) -> None:
        s = Session(role="ogretmen", user_id="t1", school_id="s1",
                    authorized_courses=frozenset({"MAT101"}))
        r = AccessRequest(action="write_grade", course_id="FIZ201", student_id="u2")
        self.assertEqual(validate_access(r, s).decision, REQUIRE_AUTHORIZATION)

    def test_teacher_authorized_course(self) -> None:
        s = Session(role="ogretmen", user_id="t1", school_id="s1",
                    authorized_courses=frozenset({"MAT101"}),
                    authorized_students=frozenset({"u2"}))
        r = AccessRequest(action="write_grade", course_id="MAT101", student_id="u2")
        self.assertEqual(validate_access(r, s).decision, ALLOW)

    def test_teacher_student_out_of_scope(self) -> None:
        s = Session(role="ogretmen", user_id="t1", school_id="s1",
                    authorized_courses=frozenset({"MAT101"}),
                    authorized_students=frozenset({"u2"}))
        r = AccessRequest(action="read_grade", course_id="MAT101", student_id="u9")
        self.assertEqual(validate_access(r, s).decision, REQUIRE_AUTHORIZATION)


class ManagerTests(unittest.TestCase):
    def test_manager_same_school(self) -> None:
        s = Session(role="yonetici", user_id="m1", school_id="s1")
        r = AccessRequest(action="read_grade", student_id="u2", school_id="s1")
        self.assertEqual(validate_access(r, s).decision, ALLOW)


if __name__ == "__main__":
    unittest.main()
