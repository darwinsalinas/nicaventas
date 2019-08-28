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
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Leon', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Chinandega', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Matagalpa', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Managua', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Granada', 't', 1);

INSERT INTO "public"."products"("sku", "description", "price") VALUES ('AZ00001', 'Paraguas de señora estampado', 10);
INSERT INTO "public"."products"("sku", "description", "price") VALUES ('AZ00002', 'Helado de sabor fresa', 1);

INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Leon', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Managua', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Chinandega', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Bluefields', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Nueva Guinea', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Juigalpa', 'AZ00001', 800, 810, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 500, 599, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 500, 599, 0.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00002', 800, 810, 1.5);
INSERT INTO "public"."rules"("country", "city", "sku", "min_condition", "max_condition", "variation") VALUES ('ni', 'Rivas', 'AZ00001', 800, 810, 0.5);