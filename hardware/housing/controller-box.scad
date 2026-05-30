// AquaWiz 제어기 하우징
// 내부 부품: 브레드보드 x2, L298N x3, Buck 5V, Buck 6V(XL4015), PWM x4
// Arduino Nano, ADS1115, HC-06은 브레드보드 위에 장착

// ==================== 파라미터 ====================

// 벽 두께
wall = 2.5;
lid_h = 3;

// 브레드보드 MB-102 (165 x 55 x 10mm) x 2개 나란히
bb_w = 165;
bb_d = 55;
bb_h = 10;
bb_gap = 5;  // 브레드보드 사이 간격

// L298N 모터드라이버 (43 x 43 x 27mm) x 3개
l298_w = 43;
l298_d = 43;
l298_h = 27;
l298_gap = 5;

// Buck 5V 컨버터 (45 x 20 x 14mm)
buck5v_w = 45;
buck5v_d = 20;
buck5v_h = 14;

// XL4015 가변 컨버터 (54 x 23 x 15mm)
xl4015_w = 54;
xl4015_d = 23;
xl4015_h = 15;

// PWM 속도 컨트롤러 (30 x 24 x 15mm) x 4개
pwm_w = 30;
pwm_d = 24;
pwm_h = 15;

// 내부 배치: 상단=브레드보드 영역, 하단=드라이버 영역
// 여유 공간
margin = 5;

// 내부 치수 계산
inner_w = bb_w + 2*margin;  // 175
inner_d = bb_d*2 + bb_gap + l298_d + l298_gap + 2*margin;  // 168
inner_h = max(l298_h, bb_h + 20) + margin;  // 42

// 외부 치수
outer_w = inner_w + 2*wall;
outer_d = inner_d + 2*wall;
outer_h = inner_h + wall;

// 나사 기둥
screw_d = 3;
post_d = 7;
post_h = 5;

// 통풍구
vent_w = 2;
vent_gap = 4;

// ==================== 모듈 ====================

module rounded_box(w, d, h, r=3) {
    hull() {
        for (x = [r, w-r], y = [r, d-r])
            translate([x, y, 0]) cylinder(h=h, r=r, $fn=20);
    }
}

module vent_slots(w, h, n=6) {
    for (i = [0:n-1])
        translate([i*(vent_w + vent_gap), 0, 5])
            cube([vent_w, wall+1, h-10]);
}

module screw_post(h) {
    difference() {
        cylinder(d=post_d, h=h, $fn=20);
        translate([0, 0, -0.1])
            cylinder(d=screw_d, h=h+0.2, $fn=20);
    }
}

module cable_hole(d=8) {
    rotate([90, 0, 0])
        cylinder(d=d, h=wall+2, $fn=20);
}

// ==================== 본체 (하단) ====================

module controller_base() {
    difference() {
        // 외벽
        rounded_box(outer_w, outer_d, outer_h);

        // 내부 공간
        translate([wall, wall, wall])
            rounded_box(inner_w, inner_d, inner_h + 1, r=2);

        // 전면 통풍구 (L298N 방열)
        translate([wall + 10, -0.5, 0])
            vent_slots(inner_w - 20, outer_h, n=15);

        // 후면 통풍구
        translate([wall + 10, outer_d - wall - 0.5, 0])
            vent_slots(inner_w - 20, outer_h, n=15);

        // 좌측 케이블 홀 (모터/솔레노이드 연결) x3
        for (i = [0:2])
            translate([-0.5, wall + margin + 20 + i*30, outer_h/2])
                rotate([0, 90, 0])
                    cylinder(d=10, h=wall+1, $fn=20);

        // 우측 DC잭 홀
        translate([outer_w - wall - 0.5, wall + margin + 15, outer_h/2])
            rotate([0, 90, 0])
                cylinder(d=12, h=wall+1, $fn=20);

        // 우측 케이블 홀 (펌프 연결)
        for (i = [0:1])
            translate([outer_w - wall - 0.5, wall + margin + 45 + i*30, outer_h/2])
                rotate([0, 90, 0])
                    cylinder(d=10, h=wall+1, $fn=20);
    }

    // 나사 기둥 (4 코너)
    corner_inset = wall + 5;
    for (pos = [[corner_inset, corner_inset],
                [outer_w - corner_inset, corner_inset],
                [corner_inset, outer_d - corner_inset],
                [outer_w - corner_inset, outer_d - corner_inset]])
        translate([pos[0], pos[1], wall])
            screw_post(inner_h - lid_h);

    // 브레드보드 지지대 (레일)
    bb_x = wall + margin;
    bb_y = wall + margin;
    for (i = [0:1]) {
        translate([bb_x, bb_y + i*(bb_d + bb_gap), wall])
            cube([bb_w, 2, post_h]);
        translate([bb_x, bb_y + i*(bb_d + bb_gap) + bb_d - 2, wall])
            cube([bb_w, 2, post_h]);
    }
}

// ==================== 뚜껑 ====================

module controller_lid() {
    difference() {
        rounded_box(outer_w, outer_d, lid_h);

        // 나사 홀
        corner_inset = wall + 5;
        for (pos = [[corner_inset, corner_inset],
                    [outer_w - corner_inset, corner_inset],
                    [corner_inset, outer_d - corner_inset],
                    [outer_w - corner_inset, outer_d - corner_inset]])
            translate([pos[0], pos[1], -0.1])
                cylinder(d=screw_d, h=lid_h+0.2, $fn=20);

        // 상단 통풍 슬롯
        for (i = [0:12])
            translate([wall + 10 + i*(vent_w + vent_gap*2), wall + 10, -0.1])
                cube([vent_w, outer_d - wall*2 - 20, lid_h + 0.2]);
    }

    // 끼움 테두리
    translate([wall + 0.3, wall + 0.3, lid_h])
        difference() {
            rounded_box(inner_w - 0.6, inner_d - 0.6, 2, r=1.5);
            translate([1.5, 1.5, -0.1])
                rounded_box(inner_w - 3.6, inner_d - 3.6, 2.2, r=1);
        }
}

// ==================== 렌더링 ====================

// 본체
controller_base();

// 뚜껑 (옆에 배치)
translate([outer_w + 20, 0, 0])
    controller_lid();

// 치수 표시 (디버그용)
echo(str("제어기 외부 치수: ", outer_w, " x ", outer_d, " x ", outer_h + lid_h, " mm"));
echo(str("내부 치수: ", inner_w, " x ", inner_d, " x ", inner_h, " mm"));
