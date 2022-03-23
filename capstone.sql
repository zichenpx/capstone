--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2022-03-23 14:18:07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 66336)
-- Name: actor_in_movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actor_in_movie (
    movie_id integer NOT NULL,
    actor_id integer NOT NULL
);


ALTER TABLE public.actor_in_movie OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 66327)
-- Name: actors; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying(256) NOT NULL,
    date_of_birth date NOT NULL,
    gender character varying
);


ALTER TABLE public.actors OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 66325)
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO postgres;

--
-- TOC entry 3011 (class 0 OID 0)
-- Dependencies: 202
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- TOC entry 201 (class 1259 OID 66319)
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying(256) NOT NULL,
    release_year integer NOT NULL,
    duration integer NOT NULL,
    imdb_rating double precision NOT NULL
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 66317)
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO postgres;

--
-- TOC entry 3012 (class 0 OID 0)
-- Dependencies: 200
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- TOC entry 2862 (class 2604 OID 66330)
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- TOC entry 2861 (class 2604 OID 66322)
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- TOC entry 3005 (class 0 OID 66336)
-- Dependencies: 204
-- Data for Name: actor_in_movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actor_in_movie (movie_id, actor_id) FROM stdin;
1	1
2	3
3	4
4	2
6	2
7	5
7	8
7	9
7	10
8	5
8	8
8	9
8	10
11	11
11	12
11	13
11	14
12	6
12	7
14	6
14	7
15	6
15	7
\.


--
-- TOC entry 3004 (class 0 OID 66327)
-- Dependencies: 203
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.actors (id, name, date_of_birth, gender) FROM stdin;
1	Audrey Hepburn	1929-05-04	F
2	Louis Koo	1970-10-21	M
3	Tom Hardy	1977-09-15	M
4	Tom Holland	1996-06-01	M
5	Anne Hethaway	1982-11-12	F
6	Robert Pattinson	1986-05-13	M
7	Zoë Isabella Kravitz	1988-12-01	F
8	Julie Andrews	1935-10-01	F
9	Hector Elizondo	1936-12-22	M
10	Heather Matarazzo	1982-11-10	F
11	Meryl Streep	1949-06-22	F
12	Emily Blunt	1983-02-23	F
13	Stanley Tucci	1960-11-11	M
14	Stanley Tucci	1960-11-11	M
15	Meryl Streep	1972-06-12	F
\.


--
-- TOC entry 3002 (class 0 OID 66319)
-- Dependencies: 201
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movies (id, title, release_year, duration, imdb_rating) FROM stdin;
1	Sabrina	1954	113	7.7
2	Dunkirk	2017	106	7.8
3	Spies in Disguise	2019	106	6.8
4	Majian	2000	100	7
6	Majian2	2000	100	7
7	The Princess Diaries	2001	115	6.3
8	The Princess Diaries 2： Royal Engagement	2004	113	5.8
10	The Devil Wears Prada	2006	109	6.9
11	The Devil Wears Prada	2006	109	6.9
12	The Batman	2022	176	8.4
14	The Batman	2022	176	8.4
9	The Devil Wears Prada	2006	109	8
15	The Batman	2022	176	8.4
\.


--
-- TOC entry 3013 (class 0 OID 0)
-- Dependencies: 202
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.actors_id_seq', 16, true);


--
-- TOC entry 3014 (class 0 OID 0)
-- Dependencies: 200
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 15, true);


--
-- TOC entry 2868 (class 2606 OID 66340)
-- Name: actor_in_movie actor_in_movie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor_in_movie
    ADD CONSTRAINT actor_in_movie_pkey PRIMARY KEY (movie_id, actor_id);


--
-- TOC entry 2866 (class 2606 OID 66335)
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- TOC entry 2864 (class 2606 OID 66324)
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- TOC entry 2870 (class 2606 OID 66346)
-- Name: actor_in_movie actor_in_movie_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor_in_movie
    ADD CONSTRAINT actor_in_movie_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(id);


--
-- TOC entry 2869 (class 2606 OID 66341)
-- Name: actor_in_movie actor_in_movie_movie_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.actor_in_movie
    ADD CONSTRAINT actor_in_movie_movie_id_fkey FOREIGN KEY (movie_id) REFERENCES public.movies(id);


-- Completed on 2022-03-23 14:18:08

--
-- PostgreSQL database dump complete
--

