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



INSERT INTO "public"."countries"("country") VALUES ('ni');

INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Leon', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Chinandega', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Matagalpa', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Managua', 't', 1);
INSERT INTO "public"."cities"("city", "active", "country_id") VALUES ('Granada', 't', 1);