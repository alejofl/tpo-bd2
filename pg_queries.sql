--- 1
SELECT T.nro_cliente, T.codigo_area, T.nro_telefono
FROM E01_TELEFONO T
JOIN E01_CLIENTE C ON T.nro_cliente = C.nro_cliente
WHERE C.nombre = 'Wanda' AND C.apellido = 'Baker';

--- 2
SELECT C.*
FROM E01_CLIENTE C
JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente;

--- 3
SELECT C.*
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
WHERE F.nro_factura IS NULL;

--- 4
SELECT DISTINCT P.*
FROM E01_PRODUCTO P
INNER JOIN E01_DETALLE_FACTURA DF ON P.codigo_producto = DF.codigo_producto;

--- 5
SELECT C.*, T.*
FROM E01_CLIENTE C
LEFT JOIN E01_TELEFONO T ON C.nro_cliente = T.nro_cliente;

--- 6
SELECT C.*, COUNT(F.nro_factura) AS cantidad_facturas
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
GROUP BY C.nro_cliente, C.nombre, C.apellido;

--- 7
SELECT F.*
FROM E01_FACTURA F
JOIN E01_CLIENTE C ON F.nro_cliente = C.nro_cliente
WHERE C.nombre = 'Pandora' AND C.apellido = 'Tate';

--- 8
SELECT DISTINCT F.*
FROM E01_FACTURA F
WHERE F.nro_factura IN (
    SELECT DF.nro_factura
    FROM E01_DETALLE_FACTURA DF
    JOIN E01_PRODUCTO P ON DF.codigo_producto = P.codigo_producto
    WHERE P.marca = 'In Faucibus Inc.'
);

--- 9
SELECT T.*, C.*
FROM E01_TELEFONO T
JOIN E01_CLIENTE C ON T.nro_cliente = C.nro_cliente;


--- 10
SELECT C.nombre, C.apellido, COALESCE(SUM(F.total_con_iva), 0) AS gasto_total_con_iva
FROM E01_CLIENTE C
LEFT JOIN E01_FACTURA F ON C.nro_cliente = F.nro_cliente
GROUP BY C.nombre, C.apellido;


--- Vista 1
CREATE VIEW FacturasOrdenadas AS
SELECT *
FROM E01_FACTURA
ORDER BY fecha;


--- Vista 2
CREATE VIEW ProductosNoFacturados AS
SELECT P.*
FROM E01_PRODUCTO P
LEFT JOIN E01_DETALLE_FACTURA DF ON P.codigo_producto = DF.codigo_producto
WHERE DF.nro_factura IS NULL;
