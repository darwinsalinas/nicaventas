CREATE TABLE "public"."countries" (
  "id" serial,
  "country" varchar(128) COLLATE "pg_catalog"."default",
  CONSTRAINT "countries_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "countries_country_key" UNIQUE ("country")
);

CREATE TABLE "public"."cities" (
  "id" serial,
  "city" varchar(128) COLLATE "pg_catalog"."default",
  "active" bool,
  "country_id" int4,
  CONSTRAINT "cities_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "cities_country_id_fkey" FOREIGN KEY ("country_id") REFERENCES "public"."countries" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE "public"."products" (
  "id" serial,
  "sku" varchar(128) COLLATE "pg_catalog"."default",
  "description" varchar(128) COLLATE "pg_catalog"."default",
  "price" float8,
  CONSTRAINT "products_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "products_sku_key" UNIQUE ("sku")
);

CREATE TABLE "public"."rules" (
  "id" serial,
  "country" varchar(128) COLLATE "pg_catalog"."default",
  "city" varchar(128) COLLATE "pg_catalog"."default",
  "sku" varchar(128) COLLATE "pg_catalog"."default",
  "min_condition" int4,
  "max_condition" int4,
  "variation" float8,
  CONSTRAINT "rules_pkey" PRIMARY KEY ("id")
);



INSERT INTO "public"."countries"("id", "country") VALUES (1, 'ni');

INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (1, 'Leon', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (2, 'Chinandega', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (3, 'Matagalpa', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (4, 'Managua', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (5, 'Granada', 't', 1);



INSERT INTO "public"."products"("id", "sku", "description", "price") VALUES (1, 'AZ00001', 'Paraguas de señora estampado', 10);
INSERT INTO "public"."products"("id", "sku", "description", "price") VALUES (2, 'AZ00002', 'Helado de sabor fresa', 1);


INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (1, 'ni', 'Leon', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (2, 'ni', 'Leon', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (3, 'ni', 'Leon', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (4, 'ni', 'Leon', 'AZ00001', 800, 810, 0.5);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (5, 'ni', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (6, 'ni', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (7, 'ni', 'Managua', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (8, 'ni', 'Managua', 'AZ00001', 800, 810, 0.5);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (9, 'ni', 'Chinandega', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (10, 'ni', 'Chinandega', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (11, 'ni', 'Chinandega', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (12, 'ni', 'Chinandega', 'AZ00001', 800, 810, 0.5);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (13, 'ni', 'Bluefields', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (14, 'ni', 'Bluefields', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (15, 'ni', 'Bluefields', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (16, 'ni', 'Bluefields', 'AZ00001', 800, 810, 0.5);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (17, 'ni', 'Nueva Guinea', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (18, 'ni', 'Nueva Guinea', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (19, 'ni', 'Nueva Guinea', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (20, 'ni', 'Nueva Guinea', 'AZ00001', 800, 810, 0.5);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (21, 'ni', 'Juigalpa', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (22, 'ni', 'Juigalpa', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (23, 'ni', 'Juigalpa', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (24, 'ni', 'Juigalpa', 'AZ00001', 800, 810, 0.5);

INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (25, 'ni', 'Rivas', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (26, 'ni', 'Rivas', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (27, 'ni', 'Rivas', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("id", "country", "city", "sku", "min_condition", "max_condition", "variation") VALUES (28, 'ni', 'Rivas', 'AZ00001', 800, 810, 0.5);