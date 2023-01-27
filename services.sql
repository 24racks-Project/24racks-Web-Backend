-- SQLite
INSERT INTO User (username, password, email, confirmation_mail, validation_code)
VALUES ("Alexis", "gAAAAABjugxtBbtGgS1h9q83lLBD62TwE0rzgsHym01sTllnEuqqsI7vdR-j_1jIn6nWkYX41Ka1EP7oeXSbhO0eGF4NFhSL6A==", "alexis.centeno@mi.unc.edu.ar", 1, "gjuxBt");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (0, "", "localhost", 3000, "Minecraft");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (1, "", "localhost", 3000, "Rust ");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (2, "", "localhost", 3000, "Terraria ");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (3, "", "localhost", 3000, "FiveM ");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (4, "", "localhost", 3000, "Team Fortress 2 ");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (5, "", "localhost", 3000, "Counter Strike: Global Offensive ");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (6, "", "localhost", 3000, "Garry's Mod");
INSERT INTO ServiceGame (id_service, logo, ip, port, name) VALUES (7, "", "localhost", 3000, "ARK: Survival Evolved");

INSERT INTO `Plan` (id_plan, store, ram, typeRenewal, price, connection, playerSlot, backupPerWeek, dataTransfer, link) VALUES (0, "5 GB", "512 MB", "monthly", 0.75, "1 Gbps", "unlimited", 1, "unlimited", "price_1MNGgIGF1QOAKEuUDJxZStBB");
INSERT INTO `Plan` (id_plan, store, ram, typeRenewal, price, connection, playerSlot, backupPerWeek, dataTransfer, link) VALUES (1, "10 GB", "1 GB", "monthly", 1.5, "1 Gbps", "unlimited", 1, "unlimited", "price_1MNGhGGF1QOAKEuU4BOPSXmS");
INSERT INTO `Plan` (id_plan, store, ram, typeRenewal, price, connection, playerSlot, backupPerWeek, dataTransfer, link) VALUES (2, "15 GB", "2 GB", "monthly", 2.75, "1 Gbps", "unlimited", 2, "unlimited", "price_1MNOlHGF1QOAKEuUynytiSEQ");
INSERT INTO `Plan` (id_plan, store, ram, typeRenewal, price, connection, playerSlot, backupPerWeek, dataTransfer, link) VALUES (3, "20 GB", "4 GB", "monthly", 5.5, "1 Gbps", "unlimited", 2, "unlimited", "price_1MNOocGF1QOAKEuUwT0fAZh5");
INSERT INTO `Plan` (id_plan, store, ram, typeRenewal, price, connection, playerSlot, backupPerWeek, dataTransfer, link) VALUES (4, "25 GB", "8 GB", "monthly", 12.5, "1 Gbps", "unlimited", 3, "unlimited", "price_1MNOpDGF1QOAKEuUdeoaKQvG");
INSERT INTO `Plan` (id_plan, store, ram, typeRenewal, price, connection, playerSlot, backupPerWeek, dataTransfer, link) VALUES (5, "30 GB", "16 GB", "monthly", 25.0, "1 Gbps", "unlimited", 3, "unlimited", "price_1MNOpnGF1QOAKEuUiKZMlrRT");

INSERT INTO Plan_ServiceGame (`plan`, servicegame) VALUES (0, 0);
INSERT INTO Plan_ServiceGame (`plan`, servicegame) VALUES (1, 0);
INSERT INTO Plan_ServiceGame (`plan`, servicegame) VALUES (2, 0);
INSERT INTO Plan_ServiceGame (`plan`, servicegame) VALUES (3, 0);
INSERT INTO Plan_ServiceGame (`plan`, servicegame) VALUES (4, 0);
INSERT INTO Plan_ServiceGame (`plan`, servicegame) VALUES (5, 0);