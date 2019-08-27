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
)
;



INSERT INTO "public"."countries"("id", "country") VALUES (1, 'ni');

INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (1, 'Leon', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (2, 'Chinandega', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (3, 'Matagalpa', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (4, 'Managua', 't', 1);
INSERT INTO "public"."cities"("id", "city", "active", "country_id") VALUES (5, 'Granada', 't', 1);