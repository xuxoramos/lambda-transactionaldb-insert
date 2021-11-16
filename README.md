# Lambda Function para inserción periódica en PostgreSQL

En mi clase de Bases de Datos no relacionales vemos, como módulo final, la construcción de Data Lakes.

Para este propósito, vamos a configurar los siguientes componentes en AWS:

1. Una instancia de EC2 con una _elastic ip_
2. Un PostgreSQL dentro de esa instancia de EC2, de acuerdo [a esta guía](https://computingforgeeks.com/how-to-install-postgresql-13-on-ubuntu/)
3. Crear una tabla de juguete que representará nuestros sistemas transaccionales
4. Crear una _lambda function_ que insertará en dicha tabla de juguete
5. Configurar un evento en AWS EventBridge para que se dispare cada 2 min y llame a la _lambda function_ de arriba

## Tabla de juguete

```sql
CREATE TABLE random_data (
	id serial4 NOT NULL,
	valor text NULL,
	fecha timestamp NULL,
	CONSTRAINT random_data_pkey PRIMARY KEY (id)
);
```

## Lambda Function

![image](https://user-images.githubusercontent.com/1316464/141932380-2b746db0-22b1-4d90-ba28-570e29813ac7.png)

![image](https://user-images.githubusercontent.com/1316464/141932505-c4b30d99-a92d-4053-9a0b-2150b856bc2e.png)

![image](https://user-images.githubusercontent.com/1316464/141932815-60230a59-33d7-418b-8b39-ef5ecb7b2086.png)

![image](https://user-images.githubusercontent.com/1316464/141932954-3044a36a-0b33-4cb3-9adb-e84b2025836b.png)

![image](https://user-images.githubusercontent.com/1316464/141933032-2c4b18ea-442c-4812-a9d1-3babe757530f.png)

Al descargar este repo, deben:

1. modificar el archivo `/db.ini` y capturar sus credenciales de su instalación de PostgreSQL
2. zipear el contenido del repo
3. subirlo a la creación de la función lambda como se muestra acá abajo

![image](https://user-images.githubusercontent.com/1316464/141933120-cc4285e6-54d2-4d16-8964-a843d5df8218.png)


## Evento en EventBridge

![image](https://user-images.githubusercontent.com/1316464/141931577-098846ed-7985-4ca7-98e4-f9528ee951a2.png)

![image](https://user-images.githubusercontent.com/1316464/141931836-4f27aec2-3d13-4de3-9eb6-e2c27b7d79de.png)

![image](https://user-images.githubusercontent.com/1316464/141932107-56a319ec-1aeb-4345-83b0-9e84ae96abc7.png)

![image](https://user-images.githubusercontent.com/1316464/141932169-ba8e3b14-0dd4-41d5-92f3-124bf823e32d.png)

![image](https://user-images.githubusercontent.com/1316464/141932249-683a1ca5-0122-4243-8ea8-06369c286b01.png)

## Listo!

Chequen su tabla, debe haber un registro cada 2 mins:

![image](https://user-images.githubusercontent.com/1316464/141933580-853e72de-88be-4648-8fa3-c1087df18d54.png)

