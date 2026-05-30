// AquaWiz 펌프 + 에어 분배기 하우징
// 내부 부품: 연동 펌프 NKP-DC-B06B x4, 3-way 솔레노이드 밸브 x2

// ==================== 파라미터 ====================

wall = 2.5;
lid_h = 3;

// NKP-DC-B06B 연동 펌프 (약 55 x 38 x 65mm, 모터 포함)
pump_w = 55;   // 폭 (좌우)
pump_d = 38;   // 깊이 (앞뒤)
pump_h = 65;   // 높이 (모터 축 방향)
pump_gap = 8;  // 펌프 사이 간격
pump_n = 4;

// 펌프 마운트 홀 (M3 나사)
pump_mount_d = 3.2;
pump_mount_dist = 30;  // 마운트 홀 간격 (추정)

// 3-way 솔레노이드 밸브 (약 15 x 10 x 20mm)
sol_w = 15;
sol_d = 10;
sol_h = 20;
sol_gap = 8;
sol_n = 2;

margin = 5;

// 레이아웃: 펌프 4개 일렬 + 솔레노이드 2개 옆에
pump_area_w = pump_n * pump_w + (pump_n - 1) * pump_gap;  // 244
sol_area_w = sol_n * sol_w + (sol_n - 1) * sol_gap;  // 74

inner_w = pump_area_w + sol_area_w + margin * 3;  // 333
inner_d = max(pump_d, sol_d) + 2*margin;  // 48
inner_h = max(pump_h, sol_h) + margin;  // 70

outer_w = inner_w + 2*wall;
outer_d = inner_d + 2*wall;
outer_h = inner_h + wall;

// 호스 홀 직경
hose_d = 6;  // 실리콘 호스 외경
air_hose_d = 5;  // 에어 호스

screw_d = 3;
post_d = 7;

// ==================== 모듈 ====================

module rounded_box(w, d, h, r=3) {
    hull() {
        for (x = [r, w-r], y = [r, d-r])
            translate([x, y, 0]) cylinder(h=h, r=r, $fn=20);
    }
}

module screw_post(h) {
    difference() {
        cylinder(d=post_d, h=h, $fn=20);
        translate([0, 0, -0.1])
            cylinder(d=screw_d, h=h+0.2, $fn=20);
    }
}

module pump_mount() {
    // 펌프 안착 가이드 (U자형)
    guide_h = 15;
    guide_w = pump_w + 1;  // 여유
    guide_d = pump_d + 1;

    difference() {
        // 외벽
        translate([-1, -1, 0])
            cube([guide_w + 2, guide_d + 2, guide_h]);
        // 내부
        translate([0, 0, wall])
            cube([guide_w, guide_d, guide_h]);
    }
}

module hose_hole() {
    rotate([90, 0, 0])
        cylinder(d=hose_d, h=wall+2, $fn=20);
}

// ==================== 본체 ====================

module pump_air_base() {
    difference() {
        rounded_box(outer_w, outer_d, outer_h);

        // 내부 공간
        translate([wall, wall, wall])
            rounded_box(inner_w, inner_d, inner_h + 1, r=2);

        // 상단 호스 홀 - 펌프 입출구 (각 펌프당 2개 = 8개)
        for (i = [0:pump_n-1]) {
            px = wall + margin + i*(pump_w + pump_gap) + pump_w/2;
            // 입구 호스
            translate([px - 10, outer_d - wall - 0.5, outer_h - 15])
                hose_hole();
            // 출구 호스
            translate([px + 10, outer_d - wall - 0.5, outer_h - 15])
                hose_hole();
        }

        // 솔레노이드 에어 홀 (입력 1 + 출력 2 x 2개)
        sol_start = wall + margin*2 + pump_area_w;
        for (i = [0:sol_n-1]) {
            sx = sol_start + i*(sol_w + sol_gap) + sol_w/2;
            // 에어 입력
            translate([sx, outer_d - wall - 0.5, outer_h - 12])
                rotate([90, 0, 0])
                    cylinder(d=air_hose_d, h=wall+2, $fn=20);
            // 에어 출력
            translate([sx, -0.5, outer_h - 12])
                rotate([-90, 0, 0])
                    cylinder(d=air_hose_d, h=wall+2, $fn=20);
        }

        // 전선 홀 (우측, 전원 + 신호)
        translate([outer_w - wall - 0.5, outer_d/2, outer_h/2])
            rotate([0, 90, 0])
                cylinder(d=12, h=wall+1, $fn=20);

        // 전선 홀 (좌측)
        translate([-0.5, outer_d/2, outer_h/2])
            rotate([0, 90, 0])
                cylinder(d=12, h=wall+1, $fn=20);
    }

    // 나사 기둥
    ci = wall + 5;
    for (pos = [[ci, ci], [outer_w-ci, ci],
                [ci, outer_d-ci], [outer_w-ci, outer_d-ci]])
        translate([pos[0], pos[1], wall])
            screw_post(inner_h - lid_h);

    // 펌프 안착 가이드
    for (i = [0:pump_n-1]) {
        px = wall + margin + i*(pump_w + pump_gap);
        py = wall + margin;
        translate([px, py, wall])
            pump_mount();
    }

    // 솔레노이드 구분벽
    translate([wall + margin*2 + pump_area_w - wall, wall, wall])
        cube([wall, inner_d, inner_h * 0.6]);
}

// ==================== 뚜껑 ====================

module pump_air_lid() {
    difference() {
        rounded_box(outer_w, outer_d, lid_h);

        // 나사 홀
        ci = wall + 5;
        for (pos = [[ci, ci], [outer_w-ci, ci],
                    [ci, outer_d-ci], [outer_w-ci, outer_d-ci]])
            translate([pos[0], pos[1], -0.1])
                cylinder(d=screw_d, h=lid_h+0.2, $fn=20);

        // 펌프 헤드 접근용 개구부 (호스 연결)
        for (i = [0:pump_n-1]) {
            px = wall + margin + i*(pump_w + pump_gap) + pump_w/2;
            translate([px - pump_w/2 + 5, wall + 5, -0.1])
                cube([pump_w - 10, inner_d - 10, lid_h + 0.2]);
        }
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

pump_air_base();

translate([0, outer_d + 20, 0])
    pump_air_lid();

echo(str("펌프+분배기 외부 치수: ", outer_w, " x ", outer_d, " x ", outer_h + lid_h, " mm"));
echo(str("내부 치수: ", inner_w, " x ", inner_d, " x ", inner_h, " mm"));
