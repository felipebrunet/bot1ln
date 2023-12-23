# BIT Mail
### Descripcion: 
### Un Bot de telegram que facilita enviar cosas pagando con BTC Lightning, en forma no custodia, usando hold invoices.
<OL>
<li>Alicia publica ofertas de envio.</li>
<li>Braulio acepta o toma oferta.</li>
<li>Braulio entrega invoice por monto.</li>
<li>Bot avisa a Alicia que oferta ha sido tomada.</li>
<li>Alicia contrata servicio de envio por monto acordado en oferta.</li>
<li>Bot genera hold invoice con el hash asociado al invoice generado por Braulio.</li>
<li>Alicia paga invoice y monto se bloquea por 24H.</li>
<li>Bob llega a buscar encomienda, Alicia se lo entrega, Braulio realiza entrega a destinatario.</li>
<li>Destinatario confirma por correo recepcion de encomienda.</li>
<li>Bot paga invoice a Braulio. Wallet de Braulio revela Pre imagen asociada al hash.</li>
<li>Bot liquida invoice pagado por Alicia con la Pre imagen obtenida en el paso anterior. Servicio se completa.</li>
</OL>
<br>
<br>
Checklist: <br>

1. Bot simple operativo DONE
   - logo DONE
   - nombre DONE
   - descripcion DONE
   - responsibidad basica DONE
   - funciones anunciadas DONE
   <br>
2. Funcionalidad para conectar nodo DONE

    - desde shell interno DONE
        - LNBITS obtener balance wallet DONE
        - LNBITS decodificar invoice
        - LNBITS pagar invoice DONE
        - LNBITS checkear invoice para status y pre imagen DONE
        - LNBITS top up wallet DONE

        - LND crear invoice normal DONE
        - LND crear hodl invoice DONE
        - LND liquidar hodl invoice DONE
        - LND cancelar hodl invoice DONE
        - LND checkear estado invoice DONE
                
    - desde script de python
        - LNBITS obtener balance wallet DONE
        - LNBITS decodificar invoice DONE
        - LNBITS pagar invoice DONE
        - LNBITS checkear invoice para status y pre imagen DONE
        - LNBITS top up wallet DONE

        - LND crear invoice normal DONE
        - LND crear hodl invoice DONE
        - LND liquidar hodl invoice DONE
        - LND cancelar hodl invoice DONE
        - LND checkear estado invoice DONE

3. Crear funciones de python dentro de bot de telegram

    - Almacenar credenciales en forma segura
    - Crear funciones lightning dentro de script principal
    - step 2 futuro: Separar funcionalidades en diferentes archivos

4. Crear botones simples en bot de telegram de funciones lightning y mostrar resultado

    - Funcion de crear invoice
    - Funcion de crear hodl invoice
    - Funcion de cancelar invoice
    - Funcion de pagar invoice
    - Funcion de checkear estado de invoice

5. Disegnar interfaz completa ofertas(botones, formularios, etc) de creacion de ofertas, y toma de ofertas

    - Boton crear ofertas guarda ofertas en BBDD con su estado. Llena formulario con datos
    - Boton ver ofertas muestra las ofertas. Las lee desde BBDD con su estado.
    - Boton tomar oferta. Esto gatilla acciones de entrega de informacion, y acciones lightning.
    - Validadores de conformidad a reglas de negocio en cada paso/proceso.

6. Disegnar interfaz de notificacion de oferente para avisarle de oferta tomada.

    - TODO

7. Disegnar proceso de actualizacion de estado de oferta

    - TODO

8. Disegnar sistema de notificacion por correo a destinatario y feedback de boton de conformidad

    - TODO

9. Disegnar sistema de registro de ofertas o servicios efectuados pasados

    - TODO
    
    
    
    
    
    
