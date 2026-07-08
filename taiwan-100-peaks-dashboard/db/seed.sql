-- Sample data for MVP database verification.
-- Dashboard statistics must be calculated from hiking_records, not hard-coded.

INSERT INTO mountains (
    hiking_note_id,
    ch_mt_name,
    ch_trail_name,
    longitude_wgs84,
    latitude_wgs84,
    trail_name,
    length_km,
    elevation_min_m,
    elevation_max_m,
    elevation_diff_m,
    country_raw
) VALUES
    (429, '武陵四秀', '桃山步道', 121.3046300, 24.4325100, 'tao_mountain', 7.90, 1883, 3325, 1442, '臺中市和平區,新竹縣尖石鄉'),
    (1746, '武陵四秀', '桃山喀拉業', 121.3213877, 24.4500307, 'tao_kalaye', 9.00, 1860, 3325, 1465, '臺中市和平區,新竹縣尖石鄉,宜蘭縣大同鄉'),
    (1737, '武陵四秀', '武陵二秀(池有,品田)', 121.2668000, 24.4282000, 'chiyou_pintian', 10.10, 1860, 3524, 1664, '臺中市和平區,新竹縣尖石鄉'),
    (1750, '北大武山', '北大武山步道', 120.7613000, 22.6270600, 'mt_beidawu', 12.00, 1550, 3090, 1540, '屏東縣瑪家鄉,屏東縣泰武鄉,臺東縣金峰鄉'),
    (1761, '塔關山', '塔關山登山步道', 120.9411900, 23.2519000, 'mt_taguan', 2.20, 2580, 3222, 642, '高雄市桃源區,臺東縣海端鄉'),
    (531, '志佳陽大山', '志佳陽大山登山步道', 121.2513600, 24.3577930, 'mt_hijiayang', 8.30, 1585, 3345, 1760, '臺中市和平區'),
    (500, '郡大山', '郡大望鄉登山步道', 120.9624900, 23.5773900, 'mt_junda', 3.70, 2865, 3265, 400, '南投縣信義鄉'),
    (1734, '雪山東峰', '雪山東峰登山山徑', 121.2720730, 24.3886870, 'mt_xue_east', 5.00, 2140, 3201, 1061, '臺中市和平區'),
    (1760, '關山嶺山', '關山嶺山登山步道', 120.9594300, 23.2709300, 'mt_guanshangling', 1.50, 2733, 3176, 443, '高雄市桃源區,臺東縣海端鄉'),
    (288, '合歡山', '合歡北峰步道', 121.2816700, 24.1815200, 'hehuan_north', 2.00, 2975, 3422, 447, '南投縣仁愛鄉,花蓮縣秀林鄉'),
    (536, '合歡山', '合歡北西步道', 121.2446000, 24.1777000, 'hehuan_north_west', 6.70, 2975, 3422, 447, '南投縣仁愛鄉,花蓮縣秀林鄉'),
    (68, '玉山', '玉山前峰登山山徑', 120.9176500, 23.4756000, 'mt_jade_front', 3.50, 2610, 3239, 629, '南投縣信義鄉,嘉義縣阿里山鄉')
ON CONFLICT (hiking_note_id) DO UPDATE SET
    ch_mt_name = EXCLUDED.ch_mt_name,
    ch_trail_name = EXCLUDED.ch_trail_name,
    longitude_wgs84 = EXCLUDED.longitude_wgs84,
    latitude_wgs84 = EXCLUDED.latitude_wgs84,
    trail_name = EXCLUDED.trail_name,
    length_km = EXCLUDED.length_km,
    elevation_min_m = EXCLUDED.elevation_min_m,
    elevation_max_m = EXCLUDED.elevation_max_m,
    elevation_diff_m = EXCLUDED.elevation_diff_m,
    country_raw = EXCLUDED.country_raw;

DELETE FROM hiking_records
WHERE trail_name = 'hehuan_north'
  AND distance_km = 14.69
  AND ascent_m = 1380
  AND descent_m = 1380
  AND duration_minutes = 592
  AND record_date = DATE '2025-10-11';

INSERT INTO hiking_records (
    trail_name,
    distance_km,
    ascent_m,
    descent_m,
    duration_minutes,
    record_date
) VALUES
    ('hehuan_north', 14.69, 1380, 1380, 592, DATE '2025-10-11');

