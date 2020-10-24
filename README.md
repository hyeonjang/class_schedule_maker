"# class_schedule_maker" 
------------------------

도메인 링크
------------------------
https://class-schedule-maker.herokuapp.com/

프로젝트의 필요성
------------------------
해당 웹서비스는 초등담임교사의 학사계획업무를 체계적으로 수행하도록 도와, 초등학교 학년별 시간표를 더 체계적으로 계획하도록 돕는 것을 목표로 합니다.

프로젝트 의존성
-----------------------
```python
INSTALLED_APPS = [
	...
	
    'bootstrap_modal_forms',
    'widget_tweaks',

]
```

Schedule Maker 기능 설명
------------------------
모든 시간표는 주차별로 구성되어 있으며, 학기를 생성한 후 학기에 따라 시간표를 인스턴스화 한 후, 내용 작성 가능하다.

1 .관리자 권한 
- 최초에 생성된 슈퍼유저에 의해 권한이 부여될 수 있으며, 관리자 권한을 받아야만 학교 정보에 관한 데이터를 수정할 수 있다.
2. 담임선생님 
- 자신이 맡은 반에 대한 시간표를 수정할 수 있다. 해당 시간에 타 선생님에 의한 교과가 배정되어 있으면 수정할 수 없다.
3. 교과선생님 & 초청강사 
- 수정 시 해당 반의 담임선생님 시간표도 함께 동기화 된다.
