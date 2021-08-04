package com.example.terrariummanager

/*
* @Authors: Diego Martínez Sánchez and Guillermo Ortega Romo
* @Description: An mobile app that will have the same funcitonality like the desktop app, with the difference that you will now control-
* the main app through this mobile app from anywhere.
*/

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.fragment.app.Fragment
import com.example.terrariummanager.fragments.Configuracion
import com.example.terrariummanager.fragments.AutomaticMode
import com.example.terrariummanager.fragments.ManualMode
import kotlinx.android.synthetic.main.activity_main.*//Se agrego en el gradle para poder importar esto

class MainActivity : AppCompatActivity() {
    private val settings= Configuracion()
    private val manual= ManualMode()
    private val auto= AutomaticMode()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        replaceFragment(settings)
    }

    private fun replaceFragment(fragment: Fragment) {
        val transaccion= supportFragmentManager.beginTransaction()
        transaccion.replace(R.id.fragment_container, fragment)
        transaccion.commit()
    }
}