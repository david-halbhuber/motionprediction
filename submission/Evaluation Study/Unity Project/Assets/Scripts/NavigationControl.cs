using System;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class NavigationControl : MonoBehaviour
{

    public QuestionnaireControl questionnaireControl;

    void Start()
    {
        GetComponent<TextMeshPro>().faceColor = new Color32(23, 207, 214, 255);
    }


    void OnTriggerEnter(Collider other)
    {
        questionnaireControl.SaveAndNextQuestion();
        gameObject.SetActive(false);

        /*if (leftHand.Contains(collider.name) || rightHand.Contains(collider.name))
        {
           questionnaireControl.LoadQuestion(questionnaireControl.currentQuestionIndex + step);
        }*/
    }
}
